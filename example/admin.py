from django.contrib import admin
from models import PolygonObject
    
class PolygonObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(PolygonObject, PolygonObjectAdmin)