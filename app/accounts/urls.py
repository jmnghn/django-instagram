from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

# app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('password_change')), name='password_change'),
    path('password_change/', views.password_change, name='password_change')
    # path('', views.temp, name='temp'),
]