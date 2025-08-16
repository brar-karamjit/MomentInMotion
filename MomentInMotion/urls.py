from django.urls import path
from . import views

urlpatterns = [
    path('', views.suggest_activity, name='suggest_activity'),
]
