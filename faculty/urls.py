from django.urls import path
from . import views

urlpatterns = [
    # /faculty/
    path('', views.faculty_view, name='faculty'),
    
    # /faculty/add/
    path('add/', views.add_faculty_view, name='add_faculty'),
    
    # /faculty/edit/1/
    path('edit/<int:pk>/', views.edit_faculty_view, name='edit_faculty'),
    
    # /faculty/delete/1/
    path('delete/<int:pk>/', views.delete_faculty_view, name='delete_faculty'),
    
    # /faculty/import/
    path('import/', views.import_faculty_csv, name='import_faculty'),
]