from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import Field
from widgets import SimplePolygonWidget

class SimplePolygonField(models.TextField):

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            #'cls': DjangoSimplePolygonEncoder,
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(SimplePolygonField, self).__init__(*args, **kwargs)

    def pre_init(self, value, obj):
        """Convert a string value to SimplePolygon only if it needs to be deserialized.
        
        SubfieldBase meteaclass has been modified to call this method instead of
        to_python so that we can check the obj state and determine if it needs to be
        deserialized"""

        if obj._state.adding and obj.pk is not None:
            if isinstance(value, basestring):
                try:
                    return SimplePolygon.loads(value, **self.load_kwargs)
                except ValueError:
                    raise ValidationError(_("Enter valid SimplePolygon"))

        return value

    def to_python(self, value):
        """The SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert SimplePolygon object to a string"""
        if self.null and value is None:
            return None
        #return SimplePolygon.dumps(value, **self.dump_kwargs)
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value, None)

    def value_from_object(self, obj):
        value = super(SimplePolygonField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.dumps_for_display(value)

    """SimplePolygonField is a generic textfield that serializes/unserializes SimplePolygon objects"""
    def dumps_for_display(self, value):
        kwargs = { "indent": 2 }
        kwargs.update(self.dump_kwargs)
        #return SimplePolygon.dumps(value, **kwargs)
        return value

    def formfield(self, **kwargs):

        if "form_class" not in kwargs:
            kwargs["form_class"] = SimplePolygonFormField

        field = super(SimplePolygonField, self).formfield(**kwargs)

        if not field.help_text:
            field.help_text = "Enter a valid SimplePolygon"

        return field

    def get_default(self):
        """
        Returns the default value for this field.

        The default implementation on models.Field calls force_unicode
        on the default, which means you can't set arbitrary Python
        objects as the default. To fix this, we just return the value
        without calling force_unicode on it. Note that if you set a
        callable as a default, the field will still call it. It will
        *not* try to pickle and encode it.

        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return copy.deepcopy(self.default)
        # If the field doesn't have a default, then we punt to models.Field.
        return super(SimplePolygonField, self).get_default()
    
class SimplePolygonFormField(Field):
    
    def __init__(self, config_name='default', *args, **kwargs):
        kwargs.update({'widget': SimplePolygonWidget()})
        super(SimplePolygonFormField, self).__init__(*args, **kwargs)
    def clean(self, value):

        if not value and not self.required:
            return None

        value = super(SimplePolygonFormField, self).clean(value)

        if isinstance(value, basestring):
            try:
                #Check SimplePolygon Format
                pass
            except ValueError:
                raise ValidationError(_("Enter valid SimplePolygon"))
        return value