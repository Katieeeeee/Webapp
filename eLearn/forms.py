from django import forms

from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['id', 'name', 'videoid','description']
        labels = {'id': 'id', 'name': 'name', 'videoid': 'videoid', 'description':'description'}
