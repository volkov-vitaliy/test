from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Article, Author, Translation, Lang


def get_translation_inline(field_name):
    class Inline(GenericTabularInline):

        model = Translation
        extra = 0
        can_delete = False
        verbose_name = field_name
        fields = ("language", "content",)

        def get_queryset(self, request):
            return Translation.objects.filter(field_name=field_name)
        
        def get_formset(self, *args, **kwargs):
            formset = super().get_formset(*args, **kwargs)
            setattr(formset, "translation_field", field_name)
            return formset
    return Inline


@admin.register(Lang)
class LangAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ("slug", "default_title",)
    raw_id_fields = ("author",)
    inlines = (get_translation_inline("title"), get_translation_inline("content"),)

    def default_title(self, obj):
        return obj.get_title(settings.DEFAULT_LANGUAGE)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.field_name = getattr(formset, "translation_field", "")
            instance.save()
        formset.save_m2m()


admin.site.register(Author)
admin.site.register(Translation)