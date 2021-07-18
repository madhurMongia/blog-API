from django.urls import path,include
from .views import RegistrationView,LogoutView
from rest_framework.authtoken import views
app_name = 'accounts'
urlpatterns = [
    path('registration/', RegistrationView.as_view()),
     path('login/', views.obtain_auth_token),
     path('logout/',LogoutView.as_view())
]
