from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.api_root, name='api_root'),
    path('posts/', api_views.post_list, name='api_post_list'),
    path('posts/<int:pk>/', api_views.post_detail, name='api_post_detail'),
]
