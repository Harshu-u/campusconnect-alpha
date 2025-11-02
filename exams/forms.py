from django import forms
from .models import Exam, Result
from students.models import Student

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'name', 'exam_type', 'exam_date', 'max_marks']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

class ResultForm(forms.ModelForm):
    """
    This form is used inside a "formset" to manage results in bulk.
    """
    marks_obtained = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-input w-full text-center'}))

    class Meta:
        model = Result
        fields = ['marks_obtained']