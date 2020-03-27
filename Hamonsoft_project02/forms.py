from django import forms
from .models import DB_impo


class DB_impoForm(forms.ModelForm):
    class Meta:
        model = DB_impo
        
        fields = ('name', 'period', 'content')