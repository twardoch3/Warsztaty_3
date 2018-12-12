from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from .models import *
from django.views.generic.edit import DeleteView


class MainRoomsView(View):
    template_name = 'conference_room/base.html'

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        # today = datetime.date.today().strftime('%Y %B %d, %A')
        ctx = {'rooms': rooms, 'rooms_list': rooms}
        return render(request, self.template_name, ctx)


class RoomAddEditView(View):
    template_name = 'conference_room/form_room.html'

    def get(self, request, id=None):
        txt = 'Create'
        ctx = {}
        if id:
            txt = 'Modify'
            room = get_object_or_404(Room, pk=id)
            ctx['room'] = room
        ctx['txt'] = txt
        return render(request, self.template_name, ctx)

    def post(self, request, id=None):
        n = request.POST.get('name')
        try:
            Room.room_name_validation(n)
        except Exception:
            error = 'Error! Name must start with letter. Marks like "?#$...etc not allowed'
            ctx = {'error': error}
            if id:
                ctx['room'] =Room.objects.get(pk=id)
            return render(request, self.template_name, ctx)

        cp = request.POST.get('capacity')
        pjt = request.POST.get('projector')
        if not pjt:
            pjt = False
        if not cp:
            cp = 0
        if int(cp) < 0:  # formularz ma pole required
            cp = cp[1:]
        if id:
            r = Room.objects.get(pk=id)  # update bedzie wyrzucac wyjatek
        else:
            r = Room()
        r.name = n
        r.capacity = cp
        r.projector = pjt
        try:
            r.save()
        except Exception:
            error = "Error! Duplicate name or invalid capacity entered."
            ctx = {'error': error}
            return render(request, self.template_name, ctx)

        return redirect(reverse('all_rooms'))


class OneRoom(View):
    template_name = 'conference_room/one_room.html'

    def get(self, request, id):
        room = get_object_or_404(Room, pk=id)
        ctx = {'room': room}
        return render(request, self.template_name, ctx)

    def post(self, request, id):
        room = get_object_or_404(Room, pk=id)
        d = request.POST.get('date')
        c = request.POST.get('comment')
        dnr = request.POST.get('days_number')
        a_rvd = [True if Reservation.objects.filter(room=room,
                                                    date=Reservation.strdate_to_dateformat(d) + datetime.timedelta(
                                                        days=i)) else False for i in
                 range(int(dnr))]
        error = None
        if d:
            if Reservation.is_past_date(d):
                error = "Error! Date can't be from the past."
            elif any(a_rvd):  # database Integrity Error
                error = 'Error! Room for your date(s) is already reserved! Choose another one.'
            else:
                for i in range(int(dnr)):
                    Reservation.objects.create(room=room,
                                               date=Reservation.strdate_to_dateformat(d) + datetime.timedelta(days=i),
                                               comment=c)
        else:
            error = 'Error! You must choose date!'

        if error:
            ctx = {'error': error, 'mr': True, 'room': room}
            return render(request, self.template_name, ctx)
        return redirect(reverse('room_reservations', kwargs={'room_id': room.id}))



class DeleteRoomView(DeleteView):
    model = Room
    # template_name =
    success_url = '/'


class DeleteReservationView(DeleteView):
    model = Reservation
    success_url = '/'  # ?


class RoomReservationsView(View):
    template_name = 'conference_room/reservations.html'

    def get(self, request, room_id, sdate=None):
        room = Room.objects.get(pk=room_id)
        if sdate:
            reservations = Reservation.objects.filter(room=room).order_by('date')
        else:
            reservations = Reservation.objects.filter(room=room).order_by('-pk')
        actual_rs = reservations.filter(date__gte=datetime.date.today())
        past_rs = reservations.filter(date__lt=datetime.date.today())
        ctx = {'room': room, 'actual_rs': actual_rs, 'past_rs': past_rs}
        return render(request, self.template_name, ctx)


class RoomSearchView(View):
    template_name = 'conference_room/search_results.html'

    def get(self, request):
        d = dict(request.GET)
        dict_search = {}
        dict_search['name__icontains'] = d['name'][0]
        dict_search['capacity__gte'] = d['capacity'][0]
        if 'projector' in d:
            if d['projector'][0] == 'Yes':
                dict_search['projector'] = True
            else:
                dict_search['projector'] = False

        dict_search = {k: v for k, v in dict_search.items() if v not in ('', [''])}
        rooms = Room.objects.filter(**dict_search)
        date = ''
        if d['date'][0]:
            reservations = Reservation.objects.filter(date=d['date'][0])
            rs_ids = [r.room.id for r in reservations]
            rooms = rooms.filter(id__in=rs_ids)
            date = d['date'][0]

        ctx = {'r': d, 'rooms': rooms, 'date': date, 'd': d}
        return render(request, self.template_name, ctx)
