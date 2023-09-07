
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ComicSerializer

# Librerías para manejar filtrado:
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Para manejar paginado:
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)



class FilteringBackendComicViewSetModel(viewsets.ModelViewSet):
    '''
    Vista de API basada en Clase que permite manejar
    el filtrado, búsqueda, paginado y orden de los resultados del
    listado de la API.
    '''
    permission_classes = (IsAuthenticated,)
    serializer_class = ComicSerializer
    http_method_names = ('get',)
    queryset = serializer_class.Meta.model.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    

    # filterset_fields = ('marvel_id',)
    filterset_fields = {
        "marvel_id": ("exact",),
        "title": ("icontains",),
        "stock_qty": ('gte',)
    }

    pagination_class = LimitOffsetPagination

    search_fields = ('title',)

    ordering_fields = ('marvel_id', 'title')
    ordering = ('-marvel_id')


class ShortResultsSetPagination(PageNumberPagination):
    page_size = 3   
    # Me va a permitir configurar la cantidad de resultados a mostrar
    # por página.
    page_size_query_param = 'page_size'
    max_page_size = 10