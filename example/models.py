from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
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
    

class Translation(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    language = models.ForeignKey(Lang, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=128, blank=False, default="")
    content = models.TextField()

    def delete(self, *args, **kwargs):
        if self.language.lang_code == settings.DEFAULT_LANGUAGE:
            raise Exception("It's not allowed to delete default language translation")
        super().delete(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id", "field_name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "field_name", "language"], 
                name="lang_field_name")
        ]
    

class TranslationField(models.TextField):

    def __init__(self, *args, **kwargs):
        kwargs["editable"] = False
        super().__init__(*args, **kwargs)

    def get_translation_for_language(self, name):
        def func(self, language_code):
            ct = ContentType.objects.get_for_model(self)
            translation = Translation.objects.filter(
                content_type=ct,
                object_id=self.id,
                language__lang_code=language_code,
                field_name=name,
            ).first()
            if translation is None:
                translation = Translation.objects.filter(
                    content_type=ct,
                    object_id=self.id,
                    language__lang_code=settings.DEFAULT_LANGUAGE,
                    field_name=name
                ).first()
                if not translation:
                    return ""
            return translation.content
        return func

    def contribute_to_class(self, cls, name):
        setattr(cls, f"get_{name}", self.get_translation_for_language(name))
        setattr(cls, f"{name}_rels", GenericRelation(Translation))
        return super().contribute_to_class(cls, name)


class Article(models.Model):

    slug = models.SlugField(db_index=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    title = TranslationField()
    content = TranslationField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

