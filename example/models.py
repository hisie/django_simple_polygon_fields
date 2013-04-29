from django.db import models
from svg_fields.fields import SVGField

# Create your models here.
class SvgObject(models.Model):
    name=models.TextField()
    svg_data=SVGField(max_length=12)