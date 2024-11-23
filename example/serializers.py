from django.conf import settings
from rest_framework import serializers

from .models import Article, Author, Translation


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ["name", "birth_date", "about", "about_short"]


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        language_code = self.context.get("lang", settings.DEFAULT_LANGUAGE)
        translation = Translation.objects.filter(
            article=obj, 
            language__lang_code=language_code,
        ).first()
        return translation.content if translation else ""

    class Meta:
        model = Article
        fields = ["title", "content", "slug", "author"]