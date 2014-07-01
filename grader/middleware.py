from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile


def get_login_url():
    return settings.LOGIN_URL

def get_exempts():
    exempts = [compile(get_login_url().lstrip('/'))]
    if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
        exempts += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
    return exempts

class LoginRequiredMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
        requires authentication middleware to be installed. Edit your\
        MIDDLEWARE_CLASSES setting to insert\
        'django.contrib.auth.middlware.AuthenticationMiddleware'. If that\
        doesn't work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
        'django.core.context_processors.auth'."
        if not request.user.is_authenticated():
            path = request.path.lstrip('/')
            if not any(m.match(path) for m in get_exempts()):
                return HttpResponseRedirect(
                            get_login_url() + "?next=" + request.path)

'''from django.http import HttpResponseRedirect
from grader.settings import LOGIN_URL

class GraderUrlMiddleware(object):
    def process_request(self, request):
        if not request.META['REMOTE_ADDR'] == "10.105.1.3":
            return
        print request.path_info
        request.path_info = request.path_info.replace("//static", "/autograder/static")
        request.path_info = request.path_info.replace("//", "/")
        print "Redirecting to {0}".format(request.path_info)
        print request.META['REMOTE_ADDR']
        #return HttpResponsePermanentRedirect(request.path)
        if not request.user.is_authenticated():
            return HttpResponseRedirect(LOGIN_URL)'''
