from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Translation, Lang


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


admin.site.register(Translation)