from django.urls import path
from .views import MainRoomsView, RoomSearchView, OneRoom, RoomAddEditView, DeleteRoomView, RoomReservationsView, DeleteReservationView

urlpatterns = [

    path('', MainRoomsView.as_view(), name="all_rooms"),

    path('room/new/', RoomAddEditView.as_view(), name="new_room"),
    path('room/edit/<int:id>', RoomAddEditView.as_view(), name='edit_room'),
    path('room/<int:id>', OneRoom.as_view(), name='room_details'),
    path('room/delete/<int:pk>', DeleteRoomView.as_view(), name='delete_room'),  # pk wymagane przez delete view
    path('reservations/<int:room_id>', RoomReservationsView.as_view(), name='room_reservations'),
    path('reservations/<int:room_id>/<int:sdate>', RoomReservationsView.as_view(), name='room_reservations_sdate'), #sort_by date
    path('search/', RoomSearchView.as_view(), name="search_room"),
    path('reservation/delete/<int:pk>', DeleteReservationView.as_view(), name='delete_reservation')

]
