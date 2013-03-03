# coding: utf-8
'''
Created on Jun 9, 2012

@author: yeti
'''
from django.contrib.localflavor.ro.forms import ROCNPField
from django.core.validators import EMPTY_VALUES
from django.core.exceptions import ValidationError

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
            checksum += int(digit) * int(value_iter.next())
        checksum %= 11
        if checksum == 10:
            checksum = 1
        if checksum != int(value[12]):
            raise ValidationError(self.error_messages['invalid'])
        return value
        