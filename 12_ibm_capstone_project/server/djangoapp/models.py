from django.utils.timezone import now
from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='car')
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.name)

class CarModel(models.Model):
    BIKE = "Bike"
    COUPE = "Coupe"
    MINIVAN = "Mini"
    OTHER = "Other"
    PICKUP = "Pickup"
    SCOOTER = "Scooter"
    SEDAN = "Sedan"
    SPORT = "Sport"
    SUV = "SUV"
    TRUCK = "Truck"
    VAN = "Van"
    WAGON = "Wagon"

    CHOICES = [
        (BIKE, "Motor Bike"), (COUPE, "Coupe"), (MINIVAN, "Mini Van"), (PICKUP, "Pick-up Truck"), (SCOOTER, "Scooter"),
        (SEDAN, "Sedan"), (SPORT, "Sports Car"), (SUV, "SUV"), (TRUCK, "Truck"), (VAN, "Van"), (WAGON, "Wagon"), (OTHER, 'Other'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer = models.IntegerField()
    name = models.CharField(max_length=60)
    car_type = models.CharField(max_length=15, choices=CHOICES, default=SUV)
    year = models.DateField(default=now)
    objects = models.Manager()

    def __str__(self):
        return str(self.name)

class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name
        
    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, dealership, id, name, purchase, review, car_make=None, car_model=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return self.name + "'s Review: " + self.review
