from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    whatsapp_number = forms.CharField(required=True, label="WhatsApp Number", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}))

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'whatsapp_number']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Automatically create or update UserProfile and save WhatsApp number
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'whatsapp_number': self.cleaned_data['whatsapp_number']}
            )
        return user