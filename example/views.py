from django.conf import settings
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from example.models import Article, Author
from example.serializers import ArticleSerializer, AuthorSerializer


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    

class ArticleViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Article.filter_by_translation(self.request.current_language)

    serializer_class = ArticleSerializer
    lookup_field = "slug"

    def list(self, request):
        articles = self.get_queryset()
        if request.GET.get('q'):
            articles = articles.filter(
                Q(translation_title__contains=request.GET.get('q'))
                | Q(translation_content__contains=request.GET.get('q'))
                | Q(author__name__contains=request.GET.get('q'))
            ).distinct()
        serializer = ArticleSerializer(articles, many=True, context={'lang': request.current_language})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug=None):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article, context={'lang': request.current_language})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer