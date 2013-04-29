# Create your views here.

from models import SvgObject
from forms import SvgObjectForm
from django.shortcuts import render

def svg_object_form(request):
    form = SvgObjectForm(request.POST)
    
    return render(request,
                  'example/form.html', 
                  {'form': form,} , 
                  content_type='text/html') 