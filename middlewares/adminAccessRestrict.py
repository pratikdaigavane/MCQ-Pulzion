from django.http import Http404, HttpResponseForbidden
from django.urls import reverse, NoReverseMatch


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# This is a middleware which allows admin access only from the server.


class adminRestrictMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_host().split(":")[0] != get_client_ip(request) and str(request.path).startswith("/admin"):
            print("Intruder trying to access AdminSite was blocked!")
            return HttpResponseForbidden()
        return self.get_response(request)
