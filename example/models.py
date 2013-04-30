from django.db import models
from simple_polygon.fields import SimplePolygonField

# Create your models here.
class PolygonObject(models.Model):
    name=models.TextField()
    svg_data=SimplePolygonField(max_length=12)