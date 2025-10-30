from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_view, name='faculty'),
    # Add path for the new view
    path('add/', views.add_faculty_view, name='add_faculty'),
]