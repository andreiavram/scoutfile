# coding: utf-8
from builtins import next

from ajax_select.fields import AutoCompleteSelectWidget, AutoCompleteSelectField, AutoCompleteSelectMultipleField, \
    AutoCompleteSelectMultipleWidget
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from localflavor.ro.forms import ROCNPField
from django.utils.translation import gettext as _


class BetterROCNPField(ROCNPField):
    
    def clean(self, value):
        """
        CNP validations
        """
        value = super(ROCNPField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        # check birthdate digits

        import datetime
        try:
            year = int(value[1:3])
            if int(value[0]) in (1, 2, 3, 4, 7, 8):
                year += 1900
            elif int(value[0]) in (5, 6):
                year += 2000
            
            datetime.date(year,int(value[3:5]),int(value[5:7]))
        except:
            raise ValidationError(self.error_messages['invalid'])
        # checksum
        key = '279146358279'
        checksum = 0
        value_iter = iter(value)
        for digit in key:
            checksum += int(digit) * int(next(value_iter))
        checksum %= 11
        if checksum == 10:
            checksum = 1
        if checksum != int(value[12]):
            raise ValidationError(self.error_messages['invalid'])
        return value


def _media(self):
    js = []
    # Unless AJAX_SELECT_BOOTSTRAP == False
    # then load include bootstrap which will load jquery and jquery ui + default css as needed
    if getattr(settings, "AJAX_SELECT_BOOTSTRAP", True):
        js.append('ajax_select/js/bootstrap.js')

    js.append('ajax_select/js/ajax_select.js')

    return forms.Media(css={'all': ('ajax_select/css/ajax_select.css',)}, js=js)


class NonAdminAutoCompleteSelectWidget(AutoCompleteSelectWidget):
    """
    Overwrite the media property of AutoCompleteSelectWidget to not include the django admin
    """
    media = property(_media)


class NonAdminMultipleAutoCompleteSelectWidget(AutoCompleteSelectMultipleWidget):
    media = property(_media)


as_default_help = 'Enter text to search.'


class NonAdminAutoCompleteSelectField(AutoCompleteSelectField):
    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        widget_kwargs = dict(
                channel=channel,
                help_text=kwargs.get('help_text', _(as_default_help)),
                show_help_text=kwargs.pop('show_help_text', True),
                plugin_options=kwargs.pop('plugin_options', {})
        )
        widget_kwargs.update(kwargs.pop('widget_options', {}))
        kwargs["widget"] = NonAdminAutoCompleteSelectWidget(**widget_kwargs)
        super(AutoCompleteSelectField, self).__init__(max_length=255, *args, **kwargs)


class NonAdminMultipleAutoCompleteSelectField(AutoCompleteSelectMultipleField):
    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

        widget_kwargs = dict(
                channel=channel,
                help_text=kwargs.get('help_text', _(as_default_help)),
                show_help_text=kwargs.pop('show_help_text', True),
                plugin_options=kwargs.pop('plugin_options', {})
        )
        widget_kwargs.update(kwargs.pop('widget_options', {}))
        kwargs["widget"] = NonAdminMultipleAutoCompleteSelectWidget(**widget_kwargs)
        super().__init__(channel, *args, **kwargs)
