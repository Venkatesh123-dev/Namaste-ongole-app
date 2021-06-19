from django.urls import path
from .views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="user_registration"),
    path('login/', UserLoginApiView.as_view(), name="user_login"),
    path('update/<int:pk>', UserProfileUpdateView.as_view(), name="user_update"),
    path('pwd_change/', ChangePasswordView.as_view(), name="change_password"),
    path('privacy/', privacy, name='privacy'),
]

