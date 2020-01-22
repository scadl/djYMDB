from django.forms import ModelForm, Textarea, SelectMultiple, RadioSelect
from .models import ArtObject, Collections, GenerTag, sysSettings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class ArtForm(ModelForm):
    class Meta:
        model = ArtObject
        fields = '__all__'
        widgets = {
            'UserRating': RadioSelect(attrs={'style':'margin-right:5px'}),
            'ArtSubTitle': Textarea(attrs={'style':'height:65px'}),
            'UserComment': Textarea(attrs={'style': 'height:130px'}),
            'ArtGeners': SelectMultiple(attrs={'style': 'height:615px'} ),
        }
        exclude = ['theUser']

class CollectionForm(ModelForm):
    class Meta:
        model = Collections
        fields = '__all__'
        exclude = ['artobject', 'theUser']


class GenerTagForm(ModelForm):
    class Meta:
        model = GenerTag
        tempFiled = [f.name for f in model._meta.get_fields()]
        tempFiled.remove('artobject')
        fields = tempFiled
        exclude = ['theUser']

class FormSettings(ModelForm):
    class Meta:
        model = sysSettings
        fields = '__all__'
        exclude = ['theUser']

class ExRegForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Укажите пожалуйста, чтобы мы знали как к вам обращаться', label='Полное имя')
    email = forms.CharField(max_length=254, required=True, help_text='Наша связь с вами. Укажите пожалуйста действующий ящик', label='Ваша Эл.Почта. (e-mail)')

    class Meta:
        model = User
        fields = ('username','first_name','email','password1','password2')
