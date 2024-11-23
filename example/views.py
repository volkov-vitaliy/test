from django.conf import settings
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from example.models import Article, Author
from example.serializers import ArticleSerializer, AuthorSerializer


def extract_language(request):
    accept_language = request.headers.get('Accept-Language', settings.DEFAULT_LANGUAGE)
    return 'ua' or accept_language.split(',')[0].split('-')[0]


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    

class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"

    def list(self, request):
        lang = extract_language(request)
        articles = self.queryset.filter(
            translation__language__lang_code=lang,
            translation__language__is_active=True
        )
        if request.GET.get('q'):
            articles = articles.filter(
                Q(translation__content__contains=request.GET.get('q')) 
                | Q(author__name__contains=request.GET.get('q'))
            ).distinct()
        serializer = ArticleSerializer(articles, many=True, context={'lang': lang})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug=None):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article, context={'lang': extract_language(request)})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer