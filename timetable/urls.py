from django.urls import path
from . import views 

app_name = 'timetable' # <-- Add app_name

urlpatterns = [
    path('', views.timetable_view, name='timetable'), 
]