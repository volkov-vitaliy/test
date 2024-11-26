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

    def _get_translation_for_language(self, field_name):
        def func(self, language_code):
            obj = type(self).filter_by_translation(language_code).filter(id=self.id).first()
            if obj is None:
                return ""
            return getattr(obj, f"translation_{field_name}", "")
        return func

    def contribute_to_class(self, cls, name):
        """Set new attributes get_FIELD into class to get translation value"""
        setattr(cls, f"get_{name}", self._get_translation_for_language(name))

        # Collection of fields with translation to track and data manipulate
        translation_fields = getattr(cls, "_translation_fields", [])
        translation_fields.append(name)
        setattr(cls, "_translation_fields", translation_fields)
        return super().contribute_to_class(cls, name)
    

class TranslationBaseModel(models.Model):

    translation = GenericRelation(Translation)

    @classmethod
    def filter_by_translation(cls, lang_code):
        """Annotate translation_FIELD to queryset. """
        # Probably most important and core function that provides 
        # high-performance functional as it uses single SQL query.
        # TranslationField uses this function as well if you want
        # to access to field value outside of this function's context
        ct = ContentType.objects.get_for_model(cls)
        queryset = cls.objects.filter(translation__language__is_active=True)    
        for field_name in getattr(cls, "_translation_fields", []):
            subquery_lang_code = Translation.objects.filter(
                object_id=models.OuterRef("id"), 
                content_type=ct,
                field_name=field_name,
                language__lang_code=lang_code,
                language__is_active=True,
            )

            subquery_default_lang = Translation.objects.filter(
                object_id=models.OuterRef("id"), 
                content_type=ct,
                field_name=field_name,
                language__lang_code=settings.DEFAULT_LANGUAGE,
            )

            # SELECT content FROM translation WHERE object = self and field_name = field_name and language = lang_code
            # SELECT content FROM translation WHERE object = self and field_name = field_name and language = default_lang_code

            # CASE
            #     WHEN Exists(subquery_lang_code) THEN subquery_lang_code.content
            #     WHEN EXISTS(subquery_default_lang) THEN subquery_default_lang.content
            #     ELSE "" 
            # END 
            # queryset = queryset.annotate(
            #     **{f"translation_{field_name}": models.Subquery(subquery)}
            # )
            queryset = queryset.annotate(
                **{
                    f"translation_{field_name}": models.Case(
                        models.When(
                            models.Exists(subquery_lang_code),
                            then=models.Subquery(subquery_lang_code.values("content"))
                        ),
                        models.When(
                            models.Exists(subquery_default_lang),
                            then=models.Subquery(subquery_default_lang.values("content"))
                        ),
                        default=models.Value(""),
                        output_field=models.TextField()
                    )
                })
        return queryset.distinct()

    class Meta:
        abstract = True