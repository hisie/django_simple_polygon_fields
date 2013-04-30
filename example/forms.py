# -*- coding: utf-8 -*-
from models import PolygonObject
from django import forms

class PolygonObjectForm(forms.ModelForm):
    class Meta:
        model = PolygonObject