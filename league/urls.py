from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('player/<int:pk>/',views.player_detail, name='player_detail'),
    path('register/',views.register,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='league/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='player_list'),name='logout'),
]