from django.urls import path
# Remove TemplateView import, add views import
# from django.views.generic import TemplateView 
from . import views # Import views from the current directory (.)

urlpatterns = [
    # Use the landing_view for the root URL
    path('', views.landing_view, name="landing"), 

    path('accounts/register/', views.register_view, name='register'),

    # Add a specific path for the dashboard
    path('dashboard/', views.dashboard_view, name="dashboard"), 

    # Update other paths to use the placeholder views
    path('students/', views.students_view, name="students"),
    path('faculty/', views.faculty_view, name="faculty"), 
    path('courses/', views.courses_view, name="courses"),
    path('timetable/', views.timetable_view, name="timetable"),
    path('attendance/', views.attendance_view, name="attendance"),
    path('exams/', views.exams_view, name="exams"),
    path('library/', views.library_view, name="library"),
    path('fees/', views.fees_view, name="fees"),
    path('hostel/', views.hostel_view, name="hostel"),
    path('sports/', views.sports_view, name="sports"),

]