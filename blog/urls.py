from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path('about/',views.about, name="about"),
    path('Create_Post/',views.create_post, name="create_post"),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),


    
]