from django import template
from django.contrib.auth.models import User, Permission

register = template.Library()


@register.filter('class_name')
def get_class_name(value: object) -> str:
    return value.__class__.__name__


@register.filter('range')
def get_range(start: int, end: int) -> range:
    return range(start, end)


@register.filter('has_perm')
def get_has_perm(user: User, permission: str or Permission) -> range:
    if isinstance(permission, Permission):
        permission = f'{permission.content_type.app_label}.{permission.codename}'
    return permission is None or user.has_perm(permission)


@register.filter('attr')
def get_attribute(obj: any, attr_name: str) -> any:
    value = obj
    for attr in attr_name.split('.'):
        if value is None:
            return None
        elif isinstance(value, dict):
            value = value.get(attr)
        elif hasattr(value, attr):
            value = getattr(value, attr)
        else:
            return None
    return value
