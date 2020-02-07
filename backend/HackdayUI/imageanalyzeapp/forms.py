from django.forms import ModelForm
from imageanalyzeapp.models import ImageModel


class ImageForm(ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']