import threading

from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin


class ThreadLocalMiddleware(MiddlewareMixin):
    def process_request(self, request):
        set_current_user(request)

    def process_response(self, request, response):
        _thread_locals.__dict__.clear()
        return response


_thread_locals = threading.local()


def get_current_user():
    if hasattr(_thread_locals, 'cached_request'):
        return get_user(_thread_locals.cached_request)
    return None


def set_current_user(request):
    _thread_locals.cached_request = request
