from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_view, name='students'),
    # Add path for the new view
    path('add/', views.add_student_view, name='add_student'),
    # add_student, edit_student, etc. will go here
]