from django.urls import path
from . import views

urlpatterns = [
    # /hostel/
    path('', views.hostel_dashboard_view, name='hostel_dashboard'),
    
    # /hostel/manage/
    path('manage/', views.manage_hostels_view, name='manage_hostels'),
    
    # /hostel/room/add/
    path('room/add/', views.add_room_view, name='add_room'),
    
    # /hostel/allocate/
    path('allocate/', views.allocate_hostel_view, name='allocate_hostel'),

    # /transport/
    path('transport/', views.transport_dashboard_view, name='transport_dashboard'),
    
    # /transport/manage/
    path('transport/manage/', views.manage_transport_view, name='manage_transport'),
    
    # /transport/allocate/
    path('transport/allocate/', views.allocate_transport_view, name='allocate_transport'),
]