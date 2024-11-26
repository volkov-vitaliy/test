from django.conf import settings
from django.contrib import admin
from translation.admin import get_translation_inline
from .models import Article, Author


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ("slug", "translation_title",)
    raw_id_fields = ("author",)
    inlines = (get_translation_inline("title"), get_translation_inline("content"),)
    
    def translation_title(self, obj):
        return obj.get_title(settings.DEFAULT_LANGUAGE)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.field_name = getattr(formset, "translation_field", "")
            instance.save()
        formset.save_m2m()


admin.site.register(Author)
