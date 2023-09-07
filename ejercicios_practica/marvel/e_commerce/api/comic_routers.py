from rest_framework.routers import DefaultRouter

from .comic_viewsets import(
    ComicViewSet,
    ComicViewSetModel,
)
from .filters import FilteringBackendComicViewSetModel

router = DefaultRouter()

router.register(
    r'viewset/comic',
    ComicViewSet,
    basename='viewset/comic'
)
router.register(
    r'modelviewset/comic',
    ComicViewSetModel,
    basename='modelviewset/comic'
)
router.register(
  r'modelviewset/filtering-backend/comics',
  FilteringBackendComicViewSetModel,
  basename='modelviewset/filtering-backend/comics'
)
urlpatterns = router.urls