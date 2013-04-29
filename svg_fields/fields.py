from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import Field
from widgets import SVGWidget

class SVGField(models.Field):

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            #'cls': DjangoSVGEncoder,
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(SVGField, self).__init__(*args, **kwargs)

    def pre_init(self, value, obj):
        """Convert a string value to SVG only if it needs to be deserialized.
        
        SubfieldBase meteaclass has been modified to call this method instead of
        to_python so that we can check the obj state and determine if it needs to be
        deserialized"""

        if obj._state.adding and obj.pk is not None:
            if isinstance(value, basestring):
                try:
                    return SVG.loads(value, **self.load_kwargs)
                except ValueError:
                    raise ValidationError(_("Enter valid SVG"))

        return value

    def to_python(self, value):
        """The SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert SVG object to a string"""
        if self.null and value is None:
            return None
        #return SVG.dumps(value, **self.dump_kwargs)
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value, None)

    def value_from_object(self, obj):
        value = super(SVGField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.dumps_for_display(value)

    """SVGField is a generic textfield that serializes/unserializes SVG objects"""
    def dumps_for_display(self, value):
        kwargs = { "indent": 2 }
        kwargs.update(self.dump_kwargs)
        #return SVG.dumps(value, **kwargs)
        return value

    def formfield(self, **kwargs):

        if "form_class" not in kwargs:
            kwargs["form_class"] = SVGFormField

        field = super(SVGField, self).formfield(**kwargs)

        if not field.help_text:
            field.help_text = "Enter a valid SVG"

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
        return super(SVGField, self).get_default()

    def db_type(self, connection):
        if connection.vendor == 'postgresql' and connection.pg_version >= 90200:
            return 'SVG'
        else:
            return super(SVGField, self).db_type(connection)
    
class SVGFormField(Field):
    
    def __init__(self, config_name='default', *args, **kwargs):
        kwargs.update({'widget': SVGWidget(config_name=config_name)})
        super(SVGFormField, self).__init__(*args, **kwargs)
    def clean(self, value):

        if not value and not self.required:
            return None

        value = super(SVGFormField, self).clean(value)

        if isinstance(value, basestring):
            try:
                #Check SVG Format
                pass
            except ValueError:
                raise ValidationError(_("Enter valid SVG"))
        return value