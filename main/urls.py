from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="home"),
    path('post/<id>/', views.post, name="post"),
    path('post/<id>/update/', views.post_update, name="post-update"),
    path('post/<id>/delete/', views.post_delete, name="post-delete"),
    path('post-create/', views.post_create, name="post-create"),
    path('search/', views.search, name="search"),
    path('blog/', views.blog, name="blog"),
]
