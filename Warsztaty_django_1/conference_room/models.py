from django.db import models
import datetime
import string


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @staticmethod
    def room_name_validation(name):
        alphabet = string.ascii_lowercase + string.ascii_uppercase
        other = '\'!@#$%^&*()_+-={}[]|\:";<>?,./'
        if name[0] not in alphabet or any([True if e in other else False for e in name]):
            raise Exception('invalid data')

    def room_today_status(self):
        if self.reservation_set.filter(date=datetime.date.today()):
            return 'reserved'
        else:
            return 'available'

    def projector_value(self):
        if self.projector:
            return 'Yes'
        else:
            return 'No'

    def room_actual_reservations(self):
        return ', '.join([str(rsv.date.strftime('%Y %b %d ')) for rsv in self.reservation_set.all() if
                          rsv.date >= datetime.date.today()])

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField()

    class Meta:
        unique_together = ('date', 'room')

    def __str__(self):
        return 'Reservation with id ' + str(self.id) + ' for ' + str(self.room)

    @staticmethod
    def strdate_to_dateformat(date):
        d_split = date.split('-')
        d_split = [int(n) for n in d_split]
        return datetime.date(d_split[0], d_split[1],
                             d_split[2])

    @staticmethod
    def is_past_date(date):
        if Reservation.strdate_to_dateformat(
                date) < datetime.date.today():
            return True
        else:
            return False
