from django.urls import path
from . import views

urlpatterns = [
    # /timetable/
    path('', views.timetable_view, name='timetable'),
    
    # /timetable/slot/add/
    path('slot/add/', views.add_timetable_slot_view, name='add_timetable_slot'),
    
    # /timetable/slot/edit/1/
    path('slot/edit/<int:pk>/', views.edit_timetable_slot_view, name='edit_timetable_slot'),
    
    # /timetable/slot/delete/1/
    path('slot/delete/<int:pk>/', views.delete_timetable_slot_view, name='delete_timetable_slot'),
]