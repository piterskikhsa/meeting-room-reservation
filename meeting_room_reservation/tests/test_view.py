import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from meeting_room_reservation.models import MeetingRoom, ReservedMeetingTime
from meeting_room_reservation.views import home_page


class ReservedMeetingTimeTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username=settings.FIRST_MANAGER_USERNAME, password="Test1234", email=settings.FIRST_MANAGER_EMAIL)
        m_id = MeetingRoom.objects.create(title='title 1', projector=True, chair_cnt=10,)
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(hours=3)
        ReservedMeetingTime.objects.create(start_meeting_time=start_time, end_meeting_time=end_time, title='title', room_id=m_id.id, user= user)


class ViewTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username=settings.FIRST_MANAGER_USERNAME, password="Test1234")

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')

        response = self.client.get(reverse('reserved', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/room/1/reserved/')

        response = self.client.get(reverse('room-edit', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/room/1/edit/')

        response = self.client.get(reverse('room-detail', kwargs={'pk': 1}))
        self.assertRedirects(response, '/login/?next=/room/1/')

        response = self.client.get(reverse('load-request'))
        self.assertRedirects(response, '/login/?next=/load-requests/')

        response = self.client.get(reverse('confirm-request', kwargs={'reserve_id': 1}))
        self.assertRedirects(response, '/login/?next=/confirm-request/1/')

        response = self.client.get(reverse('cancel-request', kwargs={'reserve_id': 1}))
        self.assertRedirects(response, '/login/?next=/cancel-request/1/')

        response = self.client.get(reverse('add-manager'))
        self.assertRedirects(response, '/login/?next=/add-manager/', kwargs={'user_id': 1})

        response = self.client.get(reverse('user-list'))
        self.assertRedirects(response, '/login/?next=/')

    def test_home_page(self):
        self.client.login(username=settings.FIRST_MANAGER_USERNAME, password="Test1234")
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), settings.FIRST_MANAGER_USERNAME)
