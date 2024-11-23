from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from example.views import ArticleViewSet, AuthorViewSet


router = routers.DefaultRouter()
router.register("authors", AuthorViewSet)
router.register("articles", ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
