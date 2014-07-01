'''
Created on Apr 19, 2014
@author: aryaveer
'''

from django import template


register = template.Library()

@register.filter
def getdictvalue(error_dict, key):
    try:
        return error_dict[key]
    except KeyError:
        return key
