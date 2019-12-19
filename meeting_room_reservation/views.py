from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView
from rolepermissions.checkers import has_permission
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.roles import assign_role

from meeting_room_reservation.forms import SignUpForm, MyForm
from meeting_room_reservation.models import MeetingRoom, ReservedMeetingTime


class UserCreatView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = '/'


class UserListView(LoginRequiredMixin, HasRoleMixin, ListView):
    model = User
    allowed_roles = 'office_manager'
    template_name = 'user_list.html'


class MeetingRoomDetailView(LoginRequiredMixin, DetailView):
    model = MeetingRoom

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).day
        approve_time = ReservedMeetingTime.objects.filter(confirmed=2, start_meeting_time__day__gte=today)\
            .order_by('start_meeting_time')
        return super().get_queryset().prefetch_related(Prefetch('meetings_time',
                                                       queryset=approve_time,
                                                       to_attr='approved_reservation'))


class MeetingRoomUpdateView(LoginRequiredMixin, HasRoleMixin, UpdateView):
    model = MeetingRoom
    allowed_roles = 'office_manager'
    fields = ('title', 'chair_cnt', 'projector', 'marker_board', 'description')


class ReservedMeetingTimeCreateView(LoginRequiredMixin, CreateView):
    model = ReservedMeetingTime
    form_class = MyForm

    def get_success_url(self):
        return reverse('room-detail', kwargs={'pk': self.object.room.pk})

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        form.instance.room = get_object_or_404(MeetingRoom, pk=self.kwargs['pk'])
        return super().form_valid(form)


@login_required(login_url='login')
def home_page(request):
    meeting_rooms = []
    confirm_requests = []
    if has_permission(request.user, 'create_reservation'):
        meeting_time_query = ReservedMeetingTime.objects.filter(confirmed=2,
                                                                start_meeting_time__gte=timezone.localtime(timezone.now())
                                                                ).order_by('start_meeting_time')
        meeting_rooms = MeetingRoom.objects.prefetch_related(Prefetch('meetings_time',
                                                                      queryset=meeting_time_query,
                                                                      ))
    if has_permission(request.user, 'confirm_reservation'):
        confirm_requests = ReservedMeetingTime.objects.filter(confirmed=1)
    return render(request, 'home_page.html', {'rooms': meeting_rooms, 'confirm_requests': confirm_requests})


@login_required(login_url='login')
@has_permission_decorator('add_new_manager')
def add_group_manager(request, user_id):
    new_manager = get_object_or_404(User, pk=user_id)
    assign_role(new_manager, 'office_manager')
    return redirect('user-list')


@csrf_exempt
@login_required(login_url='login')
@has_permission_decorator('confirm_reservation')
def load_requests(request):
    if request.is_ajax():
        confirm_requests = ReservedMeetingTime.objects.filter(confirmed=1)
        data = serializers.serialize(
            'json',
            confirm_requests,
            use_natural_foreign_keys=True,
            #todo fix room titile
            fields=('id', 'room', 'start_meeting_time', 'end_meeting_time')
        )
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
@login_required(login_url='login')
@has_permission_decorator('confirm_reservation')
def confirm_reserving_meeting_room(request, reserve_id):
    if request.is_ajax():
        reserving_time = get_object_or_404(ReservedMeetingTime, pk=reserve_id)
        reserving_time.confirm_reserving()
        #TODO send user notification
        return HttpResponse('done')
    return JsonResponse({'error': 'Method not allowed'}, status=HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
@login_required(login_url='login')
@has_permission_decorator('confirm_reservation')
def cancel_reserving_meeting_room(request, reserve_id):
    data = {}
    if request.is_ajax():
        reserving_time = get_object_or_404(ReservedMeetingTime, pk=reserve_id)
        reserving_time.cancel_reserving()
        #TODO send user notification
        data['success'] = 'done'
        return JsonResponse(data)
    data['error'] = "Method not allowed"
    return JsonResponse(data, status=HTTPStatus.METHOD_NOT_ALLOWED)
