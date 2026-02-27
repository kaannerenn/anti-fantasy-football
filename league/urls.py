from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginFormu

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('player/<int:pk>/',views.player_detail, name='player_detail'),
    path('register/',views.register,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='league/login.html',authentication_form=LoginFormu),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('add-to-team/<int:player_id>/', views.add_to_team, name='add_to_team'),
    path('my-squad/',views.my_squad,name='my_squad'),
    path('remove-player/<str:player_id>/', views.remove_from_team, name='remove_from_team'),
]