from django.db import models

#UUIDモジュールをインポートする
import uuid

#TODO:検索履歴テーブル、禁止URLテーブル、禁止タイトルテーブルを作る。

class History(models.Model):

    class Meta:
        db_table = "history"

    #UUID、検索語、検索日時、
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    search_word     = models.CharField(verbose_name="検索ワード",max_length=50)
    search_dt       = models.DateTimeField(verbose_name="期日")


    def __str__(self):
        return self.search_word

class Banurl(models.Model):

    class Meta:
        db_table = "banurl"

    #UUID、URL
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ban_url         = models.CharField(verbose_name="禁止URL",max_length=100)

    def __str__(self):
        return self.ban_url

class Bantitle(models.Model):

    class Meta:
        db_table = "bantitle"

    #UUID、TITLE
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ban_title       = models.CharField(verbose_name="禁止タイトル",max_length=100)

    def __str__(self):
        return self.ban_title


