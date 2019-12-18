from django.contrib import admin

from meeting_room_reservation.models import MeetingRoom, ReservedMeetingTime


@admin.register(ReservedMeetingTime)
class AdminReservedMeetingRoom(admin.ModelAdmin):
    list_display = ('room', 'user', 'confirmed')
    list_filter = ('confirmed', )


@admin.register(MeetingRoom)
class AdminMeetingRoom(admin.ModelAdmin):

    list_display = ('title', 'chair_cnt', 'projector', 'marker_board')
    list_filter = ('marker_board', 'projector')
    search_fields = ('title', 'description')
    list_per_page = 10

