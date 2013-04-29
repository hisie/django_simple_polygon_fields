from django.conf.urls import url, patterns

urlpatterns = patterns('', 
    url(r'^$', 'example.views.svg_object_form'),
    )

