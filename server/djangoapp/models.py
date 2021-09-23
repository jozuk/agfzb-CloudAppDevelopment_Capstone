from django.db import models
from django.utils.timezone import now
from django.conf import settings


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    country = models.CharField(max_length=50)

    def __str__(self) -> str:
        # return "Name: " + self.name + "," + \
        #     "Description: " + self.description + "," + \
        #     "Country: " + self.country
        return "Name: " + self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealerId = models.IntegerField(null=True)
    SEDAN = 'sedan'
    SUV = "suv"
    WAGON = "wagon"
    ELECTRIC = "electric"
    CAR_CATEGORIES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (ELECTRIC, "Electric")
    ]
    type = models.CharField(
        max_length=8, choices=CAR_CATEGORIES, default=SEDAN)
    year = models.DateField(default=now)
    color = models.CharField(max_length=20)

    def __str__(self):
        return "Make: " + self.make.name + "," + \
            "Name: " + self.name + "," + \
            "Dealer: " + str(self.dealerId) + "," + \
            "Type: " + self.type + "," + \
            "Color" + self.color


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer st
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, name, dealership, review, purchase, id, purchase_date=None, car_make=None, car_model=None, car_year=None, sentiment=None) -> None:
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date or None
        self.car_make = car_make or None
        self.car_model = car_model or None
        self.car_year = car_year or None
        self.sentiment = sentiment or None
        self.id = id
    
    def __str__(self):
        return "Review: " + self.review

