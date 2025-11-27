from django.urls import path
from django.urls import include
from contas import views

app_name = "contas"

urlpatterns = [
    path('token-auth/', views.CustomAuthToken.as_view(), name='token-auth'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
