from django import forms
from .models import FeeStructure, FeePayment
import datetime

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = [
            'department', 'year', 'tuition_fee', 'hostel_fee', 
            'transport_fee', 'exam_fee'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = [
            'student', 'academic_year', 'semester', 'total_amount', 
            'amount_paid', 'status', 'payment_date', 'transaction_id'
        ]
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'student': forms.HiddenInput(), # Student will be set by the view
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get current year in "YYYY-YYYY" format
        current_year = datetime.date.today().year
        default_academic_year = f"{current_year}-{current_year + 1}"
        self.fields['academic_year'].initial = default_academic_year
        self.fields['payment_date'].initial = datetime.date.today()

        for field_name, field in self.fields.items():
            if field_name != 'student':
                field.widget.attrs['class'] = 'form-input'
        
        # Make some fields not required for admins
        self.fields['payment_date'].required = False
        self.fields['transaction_id'].required = False