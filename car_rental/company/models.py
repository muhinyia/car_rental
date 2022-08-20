from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime


class Station(models.Model):

    towns = (
        ('Thika', 'Thika'),
        ('Nyahururu', 'Nyahururu'),
        ('Limuru', 'Limuru'),
        ('Mombasa', 'Mombasa'),
        ('Nairobi', 'Nairobi'),
        ('Kiambu', 'Kiambu'),
        ("Murang'a", "Murang'a"),
        ('Kerugoya', 'Kerugoya'),
        ('Kutus', 'Kutus'),
        ('Kagio', 'Kagio'),
        ('Meru', 'Meru'),
        ('Embu', 'Embu'),
        ('Kitui', 'Kitui'),
        ('Machakos', 'Machakos'),
        ('Nyeri', 'Nyeri'),
        ('Karatina', 'Karatina'),
        ('Eldoret', 'Eldoret'),
        ('Narok', 'Narok'),
        ('Kericho', 'Kericho'),
        ('Bomet', 'Bomet'),
        ('Kakamega', 'Kakamega'),
        ('Bungoma', 'Bungoma'),
        ('Busia', 'Busia'),
        ('Kisumu', 'Kisumu'),
        ('Kisii', 'Kisii'),
    )

    counties = (
        ('Mombasa', 'Mombasa'),
        ('Kwale', 'Kwale'),
        ('Kilifi', 'Kilifi'),
        ('Tana River', 'Tana River'),
        ('Lamu', 'Lamu'),
        ('Taita Taveta', 'Taita Taveta'),
        ('Garissa', 'Garissa'),
        ('Wajir', 'Wajir'),
        ('Mandera', 'Mandera'),
        ('Marsabit', 'Marsabit'),
        ('Isiolo', 'Isiolo'),
        ('Meru', 'Meru'),
        ('Tharaka Nithi', 'Tharaka Nithi'),
        ('Embu', 'Embu'),
        ('Kitui', 'Kitui'),
        ('Machakos', 'Machakos'),
        ('Makueni', 'Makueni'),
        ('Nyandarua', 'Nyandarua'),
        ('Nyeri', 'Nyeri'),
        ('Kirinyaga', 'Kirinyaga'),
        ("Murang'a", "Murang'a"),
        ('Kiambu', 'Kiambu'),
        ('Turkana', 'Turkana'),
        ('West Pokot', 'West Pokot'),
        ('Samburu', 'Samburu'),
        ('Trans-Nzoia', 'Trans-Nzoia'),
        ('Uasin Gishu', 'Uasin Gishu'),
        ('Elgeyo Marakwet', 'Elgeyo Marakwet'),
        ('Nandi', 'Nandi'),
        ('Baringo', 'Baringo'),
        ('Laikipia', 'Laikipia'),
        ('Nakuru', 'Nakuru'),
        ('Narok', 'Narok'),
        ('Kajiado', 'Kajiado'),
        ('Kericho', 'Kericho'),
        ('Bomet', 'Bomet'),
        ('Kakamega', 'Kakamega'),
        ('Vihiga', 'Vihiga'),
        ('Bungoma', 'Bungoma'),
        ('Busia', 'Busia'),
        ('Siaya', 'Siaya'),
        ('Kisumu', 'Kisumu'),
        ('Homa Bay', 'Homa Bay'),
        ('Migori', 'Migori'),
        ('Kisii', 'Kisii'),
        ('Nyamira', 'Nyamira'),
        ('Nairobi', 'Nairobi'),

    )

    name = models.CharField(max_length=100)
    county = models.CharField(
        max_length=100, choices=counties, default='Nairobi')
    town = models.CharField(max_length=100, choices=towns, default='Thika')
    mobile = models.CharField(max_length=10, unique=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Car(models.Model):
    Reg_No = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cars/%Y/%m/%d')
    available = models.BooleanField(default=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    fine_rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name


class Reservation(models.Model):

    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING)
    pick_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    has_paid = models.BooleanField(default=False)
    has_returned = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    customer_phone = models.CharField(max_length=10)
    id_number = models.CharField(max_length=9, unique=True)

    @ property
    def duration(self):
        total_days = (self.return_date-self.pick_date).days
        return total_days

    @ property
    def is_overdue(self):
        return date.today() > self.return_date

    @ property
    def overdue_by(self):
        total_days = (date.today() - self.return_date).days
        return total_days

    @ property
    def fine(self):
        fined = self.car.fine_rate * self.overdue_by
        return fined


class Contact(models.Model):
    customer = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.customer
