from django.urls import path
from . import views

urlpatterns = [
    path('', views.exams_view, name='exams'),
]