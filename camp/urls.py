from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('success-stories/', views.story_list, name='story_list'),
    path('success-stories/<int:pk>/', views.story_detail, name='story_detail'),
    path('donate/', views.donate, name='donate'),
]
