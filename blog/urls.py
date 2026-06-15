from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path('about/',views.about, name="about"),
    path("ads/", views.ad_test_lab, name="ad_test_lab"),
    path("offers/<slug:offer_slug>/", views.ad_landing_page, name="ad_landing_page"),
    path('Create_Post/',views.create_post, name="create_post"),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),


    
]
