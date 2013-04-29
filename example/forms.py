# -*- coding: utf-8 -*-
from models import SvgObject
from django import forms

class SvgObjectForm(forms.ModelForm):
    class Meta:
        model = SvgObject