from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User # Import our custom User model

class CustomUserCreationForm(UserCreationForm):
    # We can limit the role choices if we don't want anyone to sign up as an 'admin'
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        # ('admin', 'Admin'), # Optionally comment out to prevent random admin signups
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, 
                             widget=forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm'}))
    
    first_name = forms.CharField(max_length=100, required=True, 
                                 widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm'}))
    last_name = forms.CharField(max_length=100, required=True, 
                                widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm'}))
    email = forms.EmailField(required=True, 
                             widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Manually style the default fields
        for fieldname in ['username', 'password1', 'password2']:
            if fieldname in self.fields:
                self.fields[fieldname].widget.attrs.update({
                    'class': 'w-full px-3 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring'
                })