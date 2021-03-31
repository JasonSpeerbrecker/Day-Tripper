from django.db import models
import datetime
import re

# validations
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['fName']) < 2:
            errors['fName'] = "First name must be greater than 2 characters!"
        if len(postData['lName']) < 2:
            errors['lName'] = "Last name must be greater than 2 characters!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address format"
        for user in User.objects.all():
            if postData['email'] == user.email_address:
                errors['emailused'] = "This email is already in use, please try again."
        if len(postData['password']) < 9:
            errors['password'] = "Passwords must be greater than 8 characters!"
        if postData['password'] != postData['confirmPW']:
            errors['checkpassword'] = "Passwords do not match!"
        return errors

class TrailManager(models.Manager):
    def trail_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Trail name must be greater than 2 characters!"
        if len(postData['location']) < 2:
            errors['location'] = "Location name must be greater than 2 characters!"
        if len(postData['difficulty']) < 2:
            errors['difficulty'] = "Difficulty must be greater than 2 characters!"
        if len(postData['distance']) < 1:
            errors['distance'] = "Distance must be greater than 1 characters!"
        if len(postData['elevation_change']) < 1:
            errors['elevation_change'] = "Elevation change must be greater than 1 characters!"
        if len(postData['route_type']) < 2:
            errors['route_type'] = "Route type must be greater than 2 characters!"
        if len(postData['description']) < 8:
            errors['description'] = "Description must be greater than 8 characters!"
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['trip_name']) < 2:
            errors['trip_name'] = "Trip name must be greater than 2 characters!"
        date_time_obj = datetime.datetime.strptime(postData['trip_date'], '%Y-%m-%d')
        if date_time_obj < datetime.datetime.today():
            errors['trip_date'] = "Trip date must be in the future!"
        if not postData['food_list']:
            return errors
        if not postData['gear_check']:
            return errors
        return errors

class Comment(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['comment']) < 2:
            errors['comment'] = "Comments must be more than 2 characters!"

# models
class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trail(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)
    distance = models.IntegerField()
    elevation_change = models.IntegerField()
    route_type = models.CharField(max_length=255)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TrailManager()

class Trip(models.Model):
    trip_name = models.CharField(max_length=255)
    trip_date = models.DateField()
    food_list = models.TextField()
    gear_check = models.TextField()
    creator = models.ForeignKey(User, related_name="trips_created", on_delete = models.CASCADE)
    joined = models.ManyToManyField(User, related_name="trips_joined")
    trails = models.ManyToManyField(Trail, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    trail = models.ForeignKey(Trail, related_name="trail_comments", on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)