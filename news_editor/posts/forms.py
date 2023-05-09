from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import *


class PostPublishForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('publication_date',)
        widgets = {'publication_date': forms.TextInput(attrs={'type': 'datetime-local',
                                                              'class': 'form-date'})}

    def clean_publication_date(self):
        publication_date = self.cleaned_data['publication_date']
        if not publication_date or publication_date < timezone.now():
            raise forms.ValidationError('Дата публикации не может быть раньше текущей даты и времени')
        return publication_date


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'description', 'cover']
        widgets = {
            'publication_date': forms.TextInput(attrs={
                'type': 'datetime-local',
                'class': 'form-date'
            }),
            'cover': forms.FileInput(attrs={
                'accept': 'image/*',
                'required': False,
            })
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))