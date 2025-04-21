# gallery/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_view, name='upload'),
    path('slideshow/', views.slideshow_view, name='slideshow'),
    path('slideshow-data/', views.slideshow_data, name='slideshow-data'),
    path('settings/', views.settings_view, name='settings'),
]
