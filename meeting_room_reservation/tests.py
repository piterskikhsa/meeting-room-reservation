import datetime
from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from django.utils import timezone

from rolepermissions.checkers import has_role
from meeting_room_reservation.models import MeetingRoom, ReservedMeetingTime
from meeting_room_reservation.views import home_page


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


class ReservedMeetingTimeTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=settings.FIRST_MANAGER_USERNAME, password="Test1234", email=settings.FIRST_MANAGER_EMAIL)
        m_id = MeetingRoom.objects.create(title='title 1', projector=True, chair_cnt=10,)
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(hours=3)
        ReservedMeetingTime.objects.create(start_meeting_time=start_time, end_meeting_time=end_time, title='title', room_id=m_id.id, user= user)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_approve_reservation(self):
        pass
