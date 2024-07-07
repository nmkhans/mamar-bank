from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.UserRegisterView.as_view(), name = 'user-register'),
  path('login/', views.UserLoginView.as_view(), name = 'user-login'),
  path('logout/', views.user_logout, name = 'user-logout'),
  path('profile/', views.UserProfileView.as_view(), name = 'user-profile'),
  path('password-change/', views.UserPasswordChangeView.as_view(), name = 'password-change'),
]
