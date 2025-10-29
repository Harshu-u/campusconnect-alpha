# Inside: core/urls.py
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="core/dashboard.html"), name="dashboard"),
    path('students/', TemplateView.as_view(template_name="core/students.html"), name="students"),
    path('faculty/', TemplateView.as_view(template_name="core/faculty.html"), name="faculty"), # <-- Ensure this line is present
    path('courses/', TemplateView.as_view(template_name="core/courses.html"), name="courses"),
    path('timetable/', TemplateView.as_view(template_name="core/timetable.html"), name="timetable"),
    path('attendance/', TemplateView.as_view(template_name="core/attendance.html"), name="attendance"),
    path('exams/', TemplateView.as_view(template_name="core/exams.html"), 
    name="exams"),
    path('library/', TemplateView.as_view(template_name="core/library.html"), name="library"),
    path('fees/', TemplateView.as_view(template_name="core/fees.html"), 
    name="fees"),
    path('hostel/', TemplateView.as_view(template_name="core/hostel.html"), 
    name="hostel"),
    path('sports/', TemplateView.as_view(template_name="core/sports.html"),
    name="sports"),
    path('accounts/login/', TemplateView.as_view(template_name="core/accounts/login.html"),
    name="login"),
]