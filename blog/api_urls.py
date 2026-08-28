from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_post_list'),
    path('posts/<slug:slug>/', PostViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='api_post_detail'),
    path('', include(router.urls)),
]