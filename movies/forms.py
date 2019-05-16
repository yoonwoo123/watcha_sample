from django import forms
from .models import Score

class ScoreForm(forms.ModelForm):
    value = forms.FloatField(max_value=10,min_value=0)
    class Meta:
        model = Score
        fields = ['content', 'value']