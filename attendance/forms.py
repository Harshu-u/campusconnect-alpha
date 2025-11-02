from django import forms
from .models import Attendance
from students.models import Student
from courses.models import Course
import datetime

class MassAttendanceForm(forms.Form):
    """
    A form for taking attendance for an entire class at once.
    """
    course = forms.ModelChoiceField(queryset=Course.objects.none())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today)

    def __init__(self, *args, **kwargs):
        faculty = kwargs.pop('faculty', None)
        super().__init__(*args, **kwargs)

        if faculty:
            # A faculty member can only take attendance for their own courses
            self.fields['course'].queryset = Course.objects.filter(faculty=faculty, status='active')
        
        # Add Tailwind classes
        self.fields['course'].widget.attrs.update({'class': 'form-input'})
        self.fields['date'].widget.attrs.update({'class': 'form-input'})


class AttendanceRecordForm(forms.ModelForm):
    """
    A simple form for creating or updating a single attendance record.
    """
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'faculty', 'date', 'status', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'