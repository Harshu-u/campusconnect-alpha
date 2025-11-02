from django.urls import path
from . import views

urlpatterns = [
    # /exams/
    path('', views.exam_list_view, name='exams'),
    
    # /exams/add/
    path('add/', views.add_exam_view, name='add_exam'),
    
    # /exams/edit/1/
    path('edit/<int:pk>/', views.edit_exam_view, name='edit_exam'),
    
    # /exams/delete/1/
    path('delete/<int:pk>/', views.delete_exam_view, name='delete_exam'),

    # /exams/1/results/
    path('<int:exam_pk>/results/', views.manage_results_view, name='manage_results'),
]