from django.urls import path
from . import views

urlpatterns = [
    # /courses/
    path('', views.courses_view, name='courses'),
    
    # /courses/add/
    path('add/', views.add_course_view, name='add_course'),
    
    # /courses/edit/1/
    path('edit/<int:pk>/', views.edit_course_view, name='edit_course'),
    
    # /courses/delete/1/
    path('delete/<int:pk>/', views.delete_course_view, name='delete_course'),
]