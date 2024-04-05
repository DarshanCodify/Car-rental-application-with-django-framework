from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # Other relevant location information

    def __str__(self):
        return self.city
    
def car_image_path(instance, filename):
    # Get the make, model, and ID of the car
    make = instance.make
    model = instance.model
    car_id = instance.id
    # Extract the image type from the field name
    # Assuming the filename format is '<type>_<original_filename>'
    image_type = filename.split('_')[0]
    # Generate the folder path for the specific car
    car_folder = f"{make}{model}_car{car_id}"
    # Generate the filename using make, model, car ID, image type, and the original filename
    if image_type == 'car_image_primary':
        image_order = '1'
    elif image_type == 'car_image_secondary1':
        image_order = '2'
    elif image_type == 'car_image_secondary2':
        image_order = '3'
    else:
        # Handle other image types if needed
        image_order = 'other'
    filename = f"{make}{model}{car_id}{image_order}{filename}"
    # Return the path where the file will be uploaded
    return os.path.join('cars', 'images', car_folder, filename)    

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    mileage = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    car_image_primary = models.ImageField(upload_to=car_image_path, default='')
    car_image_secondary1 = models.ImageField(
        upload_to=car_image_path, blank=True)
    car_image_secondary2 = models.ImageField(
        upload_to=car_image_path, blank=True)
    locations = models.ManyToManyField(Location, related_name='cars')

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"