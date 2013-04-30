# Create your views here.

from models import PolygonObject
from forms import PolygonObjectForm
from django.shortcuts import render

def svg_object_form(request):
    form = PolygonObjectForm(request.POST)
    
    return render(request,
                  'example/form.html', 
                  {'form': form,} , 
                  content_type='text/html') 