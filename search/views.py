from django.shortcuts import render

# Create your views here.

#クラスベースのビューを作るため
from django.views import View

#スクレイピングのコードをインポート
from . import scraping 

#モデルから全てのテーブルのオブジェクトを読み込み
from .models import *

#タイムゾーンに合わせた日時を記録できる
from django.utils import timezone

import time

#Viewを継承してGET文、POST文の関数を作る
class SearchView(View):

    def reference(self):

        deny_url_list    = Banurl.objects.values_list("ban_url",flat=True)
        deny_title_list  = Bantitle.objects.values_list("ban_title",flat=True)

        return deny_url_list,deny_title_list

    def insert_word(self,word):

        posted  = History(  search_word = word,
                            search_dt   = timezone.now(),
                            )
        posted.save()



    def get(self, request, *args, **kwargs):

        deny_url_list,deny_title_list     = self.reference()

        if "search_word" in request.GET:
            if request.GET["search_word"] != "":

                start_time  = time.time()

                word                    = request.GET["search_word"]

                #検索結果を表示
                link_list,title_list    = scraping.search_google(word)

                #テンプレートで扱いやすいように整形
                data        = []
                link_list_length    = len(link_list)

                #ここで特定URL、タイトルのサイトを除外する。
                for i in range(link_list_length):
                    allow_flag = True

                    for deny in deny_url_list:
                        if deny in link_list[i]:
                            allow_flag   = False
                            break
                        
                    if allow_flag:
                        for deny in deny_title_list:
                            if deny in title_list[i]:
                                allow_flag   = False
                                break

                    if allow_flag:
                        data.append( { "url":link_list[i] , "title":title_list[i] } )


                #検索したワードを日時と共にDBへ格納
                self.insert_word(word)
    
                end_time    = int(time.time() - start_time)

                context = { "search_word"   : word,
                            "data"          : data,
                            "time"          : end_time
                            }

                return render(request,"search/results.html",context)

        return render(request,"search/base.html")

    def post(self, request, *args, **kwargs):

        pass

index       = SearchView.as_view()




#設定画面を表示、設定操作を受け付けるビュー
class ConfigView(View):

    def reference(self):

        #order_byでマイナスを指定すると、降順に切り替えることができる。
        history_data    = History.objects.order_by("-search_dt")
        banurl_data     = Banurl.objects.all()
        bantitle_data   = Bantitle.objects.all()

        context         = { "history_data"  : history_data,
                            "banurl_data"   : banurl_data, 
                            "bantitle_data" : bantitle_data,
                            }

        return context


    def get(self, request, *args, **kwargs):

        context = self.reference()
            
        return render(request,"search/config.html",context)

    def post(self, request, *args, **kwargs):

        if "ban_url" in request.POST:
            
        
            posted  = Banurl( ban_url = request.POST["ban_url"] )
            posted.save()

        if "ban_title" in request.POST:

            posted  = Bantitle( ban_title = request.POST["ban_title"] )
            posted.save()


        #BAN対象のURL、タイトルを削除する。
        
        if "ban_url_delete" in request.POST:
            
            target_id   = request.POST["ban_url_delete"].replace("-","")

            posted      = Banurl.objects.filter(id=target_id)
            posted.delete()

        if "ban_title_delete" in request.POST:

            target_id   = request.POST["ban_title_delete"].replace("-","")

            posted  = Bantitle.objects.filter(id=target_id)
            posted.delete()

        context = self.reference()

        return render(request,"search/config.html",context)


config     = ConfigView.as_view()
