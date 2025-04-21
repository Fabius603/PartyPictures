from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('login/', auth_views.LoginView.as_view(template_name='gallery/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('upload/', views.upload_view, name='upload'),
    path('slideshow/', views.slideshow_view, name='slideshow'),
    path('slideshow-data/', views.slideshow_data, name='slideshow-data'),
    path('settings/', views.settings_view, name='settings'),
]
