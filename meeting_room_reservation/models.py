from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from rolepermissions.roles import assign_role


class MeetingRoom(models.Model):
    title = models.CharField('Название комнаты', max_length=200, unique=True)
    chair_cnt = models.PositiveSmallIntegerField('Количество кресел', default=0)
    projector = models.BooleanField('Наличие проектора', default=False)
    marker_board = models.BooleanField('Наличие маркерной доски', default=False)
    description = models.TextField('Описание комнаты')

    def __str__(self):
        return '{} - {}'.format(self.title, self.chair_cnt)

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])

    def natural_key(self):
        return {'id': self.pk, 'title': self.title}


class ReservedMeetingTime(models.Model):
    RESERVED_STATUS = (
        (0, 'Отклонена'),
        (1, 'На модерации'),
        (2, 'Подтверждена'),
    )
    title = models.CharField('Название мероприятия', max_length=200)
    room = models.ForeignKey('MeetingRoom', on_delete=models.CASCADE, related_name='meetings_time')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_meeting_time = models.DateTimeField('Время начала встречи')
    end_meeting_time = models.DateTimeField('Время окончания встречи')
    confirmed = models.PositiveSmallIntegerField('Подтверждение резервирования', choices=RESERVED_STATUS, default=1)

    def __str__(self):
        return 'User: {} | room: {} | status: {} | time: {}'.format(
            self.user.get_full_name(),
            self.room.title,
            self.confirmed,
            self.start_meeting_time
        )

    def confirm_reserving(self):
        self.confirmed = 2
        self.save()
        return self.id

    def cancel_reserving(self):
        self.confirmed = 0
        self.save()
        return self.id


@receiver(post_save, sender=User)
def add_user_group(sender, instance, created, **kwargs):
    if created:
        assign_role(instance, 'employee')
        if instance.username == settings.FIRST_MANAGER_USERNAME and instance.email == settings.FIRST_MANAGER_EMAIL:
            assign_role(instance, 'office_manager')
