from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from rolepermissions.checkers import has_role


class UserPermissionTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Lev", password="Test123", email='test@te.ru')
        User.objects.create(username=settings.FIRST_MANAGER_USERNAME, password="Test1234", email=settings.FIRST_MANAGER_EMAIL)

    def test_user_has_employee_role(self):
        user = User.objects.get(username="Lev")
        manager = User.objects.get(username=settings.FIRST_MANAGER_USERNAME)
        self.assertEqual(has_role(user, 'employee'), True)
        self.assertEqual(has_role(manager, 'employee'), True)

    def test_user_has_manager_role(self):
        user = User.objects.get(username="Lev")
        manager = User.objects.get(username=settings.FIRST_MANAGER_USERNAME)
        self.assertEqual(has_role(user, 'office_manager'), False)
        self.assertEqual(has_role(manager, 'office_manager'), True)
