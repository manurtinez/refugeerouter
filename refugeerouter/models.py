from django.db import models
from django.urls import reverse
import uuid

# TODO make all contacts into mobile numbers or emails?


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=1024)
    wish_city = models.CharField(max_length=1024, blank=True)
    notes = models.TextField(max_length=1024, blank=True)
    contact_refugee = models.ForeignKey('Refugee', blank=True, null=True, related_name='primary_group', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('GroupUpdate', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


class Refugee(models.Model):
    GENDER_DIVERSE='D'
    GENDER_FEMALE='F'
    GENDER_MALE='M'
    GENDER_UNKNOWN='U'
    GENDER_CHOICES = [
        (GENDER_DIVERSE, 'Diverse'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
        (GENDER_UNKNOWN, 'Unknown'),
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=1024, blank=True)
    last_name = models.CharField(max_length=1024, blank=True)
    age = models.IntegerField(default=40)
    need_barrier_free = models.BooleanField(default=False)
    has_pets = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_UNKNOWN,
    )
    contact_data = models.CharField(max_length=1024, blank=True)
    origin = models.CharField(max_length=1024, blank=True)
    origin_checked = models.BooleanField(default=False)
    group = models.ForeignKey(Group, related_name='refugees', on_delete=models.CASCADE)
    notes = models.TextField(max_length=1024, blank=True)


    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Flat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner_first_name = models.CharField(max_length=1024)
    owner_last_name = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    max_male = models.IntegerField(default=0)
    max_kids = models.IntegerField(default=0)
    max_adults = models.IntegerField(default=0)
    min_kids_age = models.IntegerField(default=0)
    max_kids_age = models.IntegerField(default=18)
    is_interim = models.BooleanField(default=True)
    is_pets_allowed = models.BooleanField(default=True)
    is_barrier_free = models.BooleanField(default=True)
    notes = models.TextField(max_length=1024, blank=True)

    def __str__(self):
        return f'{self.address} (owned by {self.owner_last_name})'


class Booking(models.Model):
    BOOKING_STATE_CLOSED = 'C'
    BOOKING_STATE_CONFIRMED = 'F'
    BOOKING_STATE_DENIED = 'D'
    BOOKING_STATE_INHABITED = 'I'
    BOOKING_STATE_OPEN = 'O'
    BOOKING_STATE_REQUESTED = 'R'
    BOOKING_STATE_CHOICES = [
        (BOOKING_STATE_CLOSED, 'Closed'),
        (BOOKING_STATE_CONFIRMED, 'Confirmed'),
        (BOOKING_STATE_DENIED, 'Denied'),
        (BOOKING_STATE_INHABITED, 'Inhabited'),
        (BOOKING_STATE_OPEN, 'Open'),
        (BOOKING_STATE_REQUESTED, 'Requested'),
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(
        max_length=1,
        choices = BOOKING_STATE_CHOICES,
        default = BOOKING_STATE_OPEN,
    )
    notes = models.TextField(max_length=1024, blank=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        if self.flat and self.state == Booking.BOOKING_STATE_OPEN:
            return f'{self.flat} open from {self.start_date} till {self.end_date}'
        return f'{self.start_date} -> {self.end_date}'
