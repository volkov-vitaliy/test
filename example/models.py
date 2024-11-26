from django.db import models
from translation.models import TranslationBaseModel, TranslationField


class Author(models.Model):

    name = models.CharField(max_length=256)
    birth_date = models.DateField(db_index=True)
    about = models.TextField()
    about_short = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Article(TranslationBaseModel):

    slug = models.SlugField(db_index=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    title = TranslationField()
    content = TranslationField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

