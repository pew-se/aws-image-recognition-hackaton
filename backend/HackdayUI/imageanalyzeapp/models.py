from django.db import models


# Create your models here.
class ImageModel(models.Model):
    image = models.ImageField(upload_to="images")


class ImageMetaDataModel(models.Model):
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    sound = models.CharField(max_length=255)
    x1 = models.PositiveIntegerField(default=1)
    y1 = models.PositiveIntegerField(default=1)
    x2 = models.PositiveIntegerField(default=1)
    y2 =models.PositiveIntegerField(default=1)
