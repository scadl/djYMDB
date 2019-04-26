from django.forms import ModelForm, Textarea, SelectMultiple, RadioSelect
from .models import ArtObject, Collections, GenerTag, sysSettings


class ArtForm(ModelForm):
    class Meta:
        model = ArtObject
        fields = '__all__'
        widgets = {
            'UserRating': RadioSelect(attrs={'style':'margin-right:5px'}),
            'ArtSubTitle': Textarea(attrs={'style':'height:65px'}),
            'UserComment': Textarea(attrs={'style': 'height:130px'}),
            'ArtGeners': SelectMultiple(attrs={'style': 'height:615px'}, choices=ArtObject.ART_STATUSES, ),
        }

class CollectionForm(ModelForm):
    class Meta:
        model = Collections
        fields = '__all__'
        exclude = ['artobject']


class GenerTagForm(ModelForm):
    class Meta:
        model = GenerTag
        tempFiled = [f.name for f in model._meta.get_fields()]
        tempFiled.remove('artobject')
        fields = tempFiled

class FormSettings(ModelForm):
    class Meta:
        model = sysSettings
        fields = '__all__'
        exclude = ['theUser']
