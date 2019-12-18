from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from meeting_room_reservation import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.UserCreatView.as_view(), name='signup'),
    path('room/<int:pk>/reserved/', views.ReservedMeetingTimeCreateView.as_view(), name='reserved'),
    path('room/<int:pk>/edit/', views.MeetingRoomUpdateView.as_view(), name='room-edit'),
    path('room/<int:pk>/', views.MeetingRoomDetailView.as_view(), name='room-detail'),
    path('load-requests/', views.load_requests, name='load-request'),
    path('confirm-request/<int:reserve_id>/', views.confirm_reserving_meeting_room, name='confirm-request'),
    path('cancel-request/<int:reserve_id>/', views.cancel_reserving_meeting_room, name='cancel-request'),
    path('add-manager/<int:user_id>/', views.add_group_manager, name='add-manager'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('', views.home_page, name='home'),
]
