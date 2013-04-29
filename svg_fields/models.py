from django.db import models

# Create your models here.

class SvgField(models.TextField):
    description = "A SVG document"