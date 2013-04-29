from django.contrib import admin
from models import SvgObject
    
class SvgObjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(SvgObject, SvgObjectAdmin)