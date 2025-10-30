from django.urls import path
from . import views

urlpatterns = [
    path('', views.fees_view, name='fees'),
]