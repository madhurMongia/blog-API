from django.urls import path,include
from .views import PostListView,PostDetialView,PostUserView
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'dashboard' ,PostUserView,basename = 'post')
app_name = "api"
urlpatterns = [
    path('', PostListView.as_view()),
    path('<slug:slug>',PostDetialView.as_view()),
]
urlpatterns += router.urls