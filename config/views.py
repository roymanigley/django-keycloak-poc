from django.http import HttpResponseRedirect


def page_not_found_view(request, exception=None):
    return HttpResponseRedirect(redirect_to='/404/')


def page_permission_denied_view(request, exception=None):
    return HttpResponseRedirect(redirect_to='/403/')


def page_unexpected_error_view(request, exception=None):
    return HttpResponseRedirect(redirect_to='/500/')
