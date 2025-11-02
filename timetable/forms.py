from django import forms
from .models import TimetableSlot
from students.models import Department

class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = [
            'department', 'course', 'faculty', 'day_of_week', 
            'start_time', 'end_time', 'room_number', 'year', 'semester'
        ]
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

        # Dynamically filter courses based on the selected department
        # This will require some JavaScript on the frontend, but we set up the backend logic here.
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['course'].queryset = Course.objects.filter(department_id=department_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from browser; ignore and fallback to empty Course queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.department.courses.order_by('title')
        else:
            self.fields['course'].queryset = Course.objects.none()