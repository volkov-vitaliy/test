from django.contrib import admin
from .models import Article, Author, Translation, Lang


class TitleInline(admin.TabularInline):

    model = Translation
    extra = 0
    can_delete = False


@admin.register(Lang)
class LangAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    raw_id_fields = ("author",)
    inlines = (TitleInline,)


admin.site.register(Author)
admin.site.register(Translation)