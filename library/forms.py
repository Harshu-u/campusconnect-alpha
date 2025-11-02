from django import forms
from .models import Book, BookIssue
from students.models import Student
import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'total_copies', 'available_copies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

class BookIssueForm(forms.ModelForm):
    # We use a custom field to find the student by their ID
    student_id = forms.CharField(
        label="Student ID", 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Student ID'})
    )
    
    # This field will be hidden, we'll populate it from the student_id
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BookIssue
        fields = ['book', 'student_id', 'student', 'issue_date', 'due_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].widget.attrs.update({'class': 'form-input'})
        self.fields['issue_date'].initial = datetime.date.today()
        self.fields['due_date'].initial = datetime.date.today() + datetime.timedelta(days=14)

    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
                cleaned_data['student'] = student
            except Student.DoesNotExist:
                self.add_error('student_id', "No student found with this ID.")
        
        return cleaned_data