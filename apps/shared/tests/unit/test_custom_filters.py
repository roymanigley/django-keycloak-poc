import unittest
from dataclasses import dataclass
from unittest.mock import Mock

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.shared.templatetags.custom_filters import get_has_perm, get_range, get_class_name, get_attribute


class CustomFiltersTest(unittest.TestCase):

    def test_get_class_name(self):
        # WHEN
        class_name_page = get_class_name(Page(title="Page"))
        class_name_None = get_class_name(None)
        # THEN
        self.assertEqual(class_name_page, 'Page')
        self.assertEqual(class_name_None, 'NoneType')

    def test_get_range(self):
        # WHEN
        range_1_to_6 = get_range(1, 6)
        # THEN
        self.assertListEqual(list(range_1_to_6), list(range(1, 6)))

    def test_get_has_perm__should_be_allowed(self):
        # GIVEN
        given_permissions = [
            'fancy.permission'
        ]
        user = Mock()
        user.has_perm = lambda perm: perm in given_permissions
        permission = Permission(content_type=ContentType(app_label='fancy'), codename='permission')
        # WHEN
        valid_permission_by_str = get_has_perm(user, 'fancy.permission')
        valid_permission_by_permission_obj = get_has_perm(user, permission)
        valid_permission_by_none = get_has_perm(user, None)
        # THEN
        self.assertTrue(valid_permission_by_str)
        self.assertTrue(valid_permission_by_permission_obj)
        self.assertTrue(valid_permission_by_none)

    def test_get_has_perm__should_not_be_allowed(self):
        # GIVEN
        given_permissions = [
            'fancy.permission'
        ]
        user = Mock()
        user.has_perm = lambda perm: perm in given_permissions
        permission = Permission(content_type=ContentType(app_label='fancy'), codename='permizzion')
        # WHEN
        valid_permission_by_str = get_has_perm(user, 'not-fancy.permission')
        valid_permission_by_permission_obj = get_has_perm(user, permission)
        # THEN
        self.assertFalse(valid_permission_by_str)
        self.assertFalse(valid_permission_by_permission_obj)

    def test_get_attribute(self):
        # GIVEN
        some_dict = {'a': 'A', 'b': {'c': 'C'}}
        some_class = Page(title='some_page')
        some_class.box = Box(name='some_box')
        # WHEN
        existing_dict_attribute_value = get_attribute(some_dict, 'a')
        existing_nested_dict_attribute_value = get_attribute(some_dict, 'b.c')
        non_existing_nested_dict_attribute_value = get_attribute(some_dict, 'x.y.z')
        non_existing_dict_attribute_value = get_attribute(some_dict, 'x')
        # THEN
        existing_class_attribute_value = get_attribute(some_class, 'title')
        existing_nested_class_attribute_value = get_attribute(some_class, 'box.name')
        non_existing_nested_class_attribute_value = get_attribute(some_class, 'x.y.z')
        non_existing_class_attribute_value = get_attribute(some_class, 'blaaaa')

        self.assertEqual(existing_dict_attribute_value, 'A')
        self.assertEqual(existing_nested_dict_attribute_value, 'C')
        self.assertIsNone(non_existing_nested_dict_attribute_value)
        self.assertIsNone(non_existing_dict_attribute_value)

        self.assertEqual(existing_class_attribute_value, 'some_page')
        self.assertEqual(existing_nested_class_attribute_value, 'some_box')
        self.assertIsNone(non_existing_nested_class_attribute_value)
        self.assertIsNone(non_existing_class_attribute_value)

@dataclass
class Page:
    title: str

@dataclass
class Box:
    name: str
