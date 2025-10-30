from django.urls import path
from . import views 

urlpatterns = [
    # This path will now correctly match 'courses/' 
    # and point to your 'courses_view'
    path('', views.courses_view, name="courses"), 
    
    # We will add add_course, edit_course, etc. here in Phase 3
]