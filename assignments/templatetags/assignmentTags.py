'''
Created on May 30, 2013
@author: aryaveer
'''
from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_str
from django.template.base import kwarg_re
#from django.utils.html import conditional_escape
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django import template
import os, urllib

register = template.Library()

@register.filter
def getlen(value):
    return len(value)
    
@register.filter
def getfilename(value):
    return os.path.basename(value.name)

@register.filter
@stringfilter
def spacify(value):
    result = ''
    prev = None
    for ch in value:
        if ch == ' ' and (prev == ' ' or prev == '\n'):
            result += "&nbsp;"
            prev = ' '
        elif ch == '\n':
            result += "</br>"
            prev = '\n'
        else:
            result += ch
            prev = ''

    return mark_safe(result)
    '''if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '&'+'nbsp;', esc(value)))'''
#spacify.needs_autoescape = True

@register.tag(name="urlwithgetparam")
def urlwithgetparam(parser, token):
    bits = token.split_contents()
    viewname = bits[1]
    args = []
    kwargs = {}
    bits = bits[2:]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise Exception("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return MyUrlNode(viewname, args, kwargs, legacy_view_name=True)

class MyUrlNode(template.Node):
    def __init__(self, view_name, args, kwargs, legacy_view_name=True):
        self.view_name = view_name
        self.legacy_view_name = legacy_view_name
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        view_name = self.view_name
        if not self.legacy_view_name:
            view_name = view_name.resolve(context)

        url = reverse(view_name, args=args, current_app=context.current_app)
        if not isinstance(kwargs['get_params'], dict):
            raise Exception("get_params must be a dictionary")
        return url + '?' + urllib.urlencode(kwargs['get_params'])