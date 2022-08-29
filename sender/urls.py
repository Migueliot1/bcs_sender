from django.urls import path
from . import views

urlpatterns = [
    path('', views.showIndex, name='index'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
]
