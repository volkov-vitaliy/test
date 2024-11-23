from django.conf import settings
from django.db import models


class Lang(models.Model):

    lang_code = models.CharField(max_length=5)
    is_active = models.BooleanField(db_index=True)

    def __str__(self):
        return self.lang_code

    def delete(self, *args, **kwargs):
        if self.lang_code == settings.DEFAULT_LANGUAGE:
            raise Exception("It's not allowed to delete default language translation")
        super().delete(*args, **kwargs)


class Author(models.Model):

    name = models.CharField(max_length=256)
    birth_date = models.DateField(db_index=True)
    about = models.TextField()
    about_short = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Article(models.Model):

    slug = models.SlugField(db_index=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Translation(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE)
    content = models.TextField()