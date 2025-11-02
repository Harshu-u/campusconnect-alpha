from django.urls import path
from . import views

urlpatterns = [
    # /attendance/
    path('', views.attendance_dashboard_view, name='attendance_dashboard'),
    
    # /attendance/take/
    path('take/', views.take_attendance_view, name='take_attendance'),
    
    # We don't have views for these yet, but we'll add the URLs
    # path('edit/<int:pk>/', views.edit_attendance_view, name='edit_attendance'),
    # path('delete/<int:pk>/', views.delete_attendance_view, name='delete_attendance'),
]