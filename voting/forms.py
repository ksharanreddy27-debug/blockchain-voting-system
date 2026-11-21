from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import VoterProfile
class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    voter_id=forms.CharField(max_length=40,label='Demo voter ID')
    class Meta: model=User; fields=('username','email','voter_id','password1','password2')
    def save(self, commit=True):
        user=super().save(commit=False); user.email=self.cleaned_data['email']
        if commit:
            user.save(); VoterProfile.objects.create(user=user,voter_id=self.cleaned_data['voter_id'])
        return user
