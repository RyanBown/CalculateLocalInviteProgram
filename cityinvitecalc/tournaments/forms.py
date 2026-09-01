from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['pokemon_id','first_name','last_name','birth_year']