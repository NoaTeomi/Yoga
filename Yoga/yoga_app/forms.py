from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import YogaSequence, YogaPose

class YogaSequenceForm(forms.ModelForm):
    poses = forms.ModelMultipleChoiceField(
    queryset=YogaPose.objects.all(),
    widget=forms.CheckboxSelectMultiple,  # You can also use a select widget if preferred
    required=False
    )
    
    class Meta:
        model = YogaSequence
        fields = ['name', 'poses']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
