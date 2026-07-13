from django.urls import path
from . import views



urlpatterns = [
    path("<slug:slug>/", views.post_detail, name='post_detail' ),
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path("category/<slug:slug>/",
     views.category_posts,
     name="category_posts"),

path("tag/<slug:slug>/",
     views.tag_posts,
     name="tag_posts"),
    ]