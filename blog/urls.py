from django.urls import path
from . import views

# 127.0.0.1:8000/blog
urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('tag/<blog_tag>/', views.blog_tag, name='blog_tag'),
    path('<int:blog_pk>/', views.blog_detail, name='blog_detail'),
    path('date/<int:year>/<int:month>/', views.blog_date, name='blog_date'),
]
