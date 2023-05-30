from django.shortcuts import get_object_or_404
from titles.models import Category, Genre, Title
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
#   serializer_class = TitleSerializer
#   permission_classes = 
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
#   serializer_class = CategorySerializer
#   permission_classes = 


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
#   serializer_class = CategorySerializer
#   permission_classes = 