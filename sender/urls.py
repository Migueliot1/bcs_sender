from django.urls import path
from . import views

urlpatterns = [
    path('', views.showIndex, name='index'),
]
