from django.urls import path
from . import views

urlpatterns = [
    path('', views.sports_view, name='sports'),
]