from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.core.exceptions import ImproperlyConfigured
from django.forms.util import flatatt
import json


json_encode = json.JSONEncoder().encode


class SimplePolygonWidget(forms.Textarea):
    """
    Widget providing CKEditor for Rich Text Editing.
    Supports direct image uploads and embed.
    """
    class Media:
        try:
            js = (
                settings.STATIC_URL + 'simple_polygon/js/jsDraw2D.js',
                settings.STATIC_URL + 'simple_polygon/js/canvas_to_input.js',
            )
        except AttributeError:
            raise ImproperlyConfigured("simple_polygon requires \
                    static files correctly configured")

    #TODO: Render the widget.
    def render(self, name, value, attrs={}):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(render_to_string('simple_polygon/widget.html', {
            'final_attrs': flatatt(final_attrs),
            'value': conditional_escape(force_unicode(value)),
            #'id': final_attrs['id'],
            #'config': json_encode(self.config)
        }))