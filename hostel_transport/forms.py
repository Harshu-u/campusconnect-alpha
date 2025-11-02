from django import forms
from .models import Hostel, Room, HostelAllocation, TransportRoute, TransportAllocation
from students.models import Student

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hostel', 'room_number', 'capacity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

class HostelAllocationForm(forms.ModelForm):
    student_id = forms.CharField(
        label="Student ID", 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Student ID'})
    )
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = HostelAllocation
        fields = ['student_id', 'student', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].widget.attrs.update({'class': 'form-input'})

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
                cleaned_data['student'] = student
                
                # Check if student is already allocated
                if HostelAllocation.objects.filter(student=student).exists():
                    self.add_error('student_id', "This student already has a hostel allocation.")
                    
            except Student.DoesNotExist:
                self.add_error('student_id', "No student found with this ID.")
        
        return cleaned_data

class TransportRouteForm(forms.ModelForm):
    class Meta:
        model = TransportRoute
        fields = ['route_name', 'bus_number', 'driver_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
        self.fields['driver_name'].required = False


class TransportAllocationForm(forms.ModelForm):
    student_id = forms.CharField(
        label="Student ID", 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Student ID'})
    )
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = TransportAllocation
        fields = ['student_id', 'student', 'route']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route'].widget.attrs.update({'class': 'form-input'})

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
                cleaned_data['student'] = student
                
                # Check if student is already allocated
                if TransportAllocation.objects.filter(student=student).exists():
                    self.add_error('student_id', "This student already has a transport allocation.")
                    
            except Student.DoesNotExist:
                self.add_error('student_id', "No student found with this ID.")
        
        return cleaned_data