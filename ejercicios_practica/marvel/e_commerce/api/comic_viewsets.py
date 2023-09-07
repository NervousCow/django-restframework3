from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

# Libreria para manejar filtrado
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Libreria para manejar paginado
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

from e_commerce.models import Comic, WishList
from .serializers import ComicSerializer, WishListSerializer, UserSerializer

class ComicViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSerializer
    queryset = Comic.objects.all()

    @action(detail=False, methods=['GET'])
    def list_comics(self, request):
        serializer = self.serializer_class(self.queryset, many=True, context={'view':self})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

   
    @action(detail=False, methods=['POST'])
    def create_comic(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['PATCH'])
    def update_comic(self, request, pk=None):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['DELETE'])
    def del_comic(self, request, pk=None):
        comic = self.get_object()
        comic.delete()
        return Response(
            {"message":"El comic se borro correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )

class ComicViewSetModel(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ComicSerializer
    http_method_names = ['get']
    queryset = serializer_class.Meta.model.objects.all()

# EJERCICIO 4

class UserFavCartComic(viewsets.generics.ListAPIView):
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated]

    # Sobre-escribo el metodo get_queryset para filtrar según mis requerimientos.
    def get_queryset(self):

        # Parametro estático para la búsqueda
        user_id = 1

        # Definiciones de los filtros
        favorites = Comic.objects.filter(wishlist__user=user_id, wishlist__favorite=True)
        cart = Comic.objects.filter(wishlist__user=user_id, wishlist__cart=True)

        # Combinaciones de los filtros para devolver un queryset
        # queryset = Comic.objects.filter(id__in=favorites) | Comic.objects.filter(id__in=cart)

        # queryset = favorites.intersection(cart)

        queryset = favorites & cart

        return queryset