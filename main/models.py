from django.db import models
from datetime import date, datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def basicvalidator(self, postData):
        regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        letters = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 3:
            errors['name'] = "The name must be 3 letters at least";
        if len(postData['nickname']) < 3:
            errors['nickname'] = "The username name must be 3 letters at least";
        if not regex.match(postData['email']):
            errors['email'] = "invalid e-mail"
        if not letters.match(postData['name']):
            errors['solo_letras'] = "Your name must be only Letters"
        if len(postData['password']) < 8:
            errors['password'] = "The password must be 8 characters at least";
        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "Both Passwords must be equals "
        return errors

class TravelManager(models.Manager):
    def basicvalidator(self, postData):
        today = date.today().strftime("%Y-%m-%d")
        start_date = postData['start_date']
        errors = {}

        if len(postData['destination']) < 1:
            errors['destination'] = "The destination must not be empty";
        if len(postData['description']) < 1:
            errors['description'] = "The description must not be empty";
        if (postData['start_date']) < today:
            errors["start_date"] = "The trip can't start before today!"
        if (postData['end_date']) < start_date :
            errors["end_date"] = "The trip must finish after the start!"
        if (postData['start_date']) == "":
            errors["start_date"] = "The datefield can't be empty"
        if (postData['end_date']) == "":
            errors["end_date"] = "The datefield can't be empty"

        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.URLField(default='https://toppng.com/uploads/preview/roger-berry-avatar-placeholder-11562991561rbrfzlng6h.png')
    password = models.CharField(max_length=70)
    # travels
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.nickname}"

    def __repr__(self):
        return f"{self.nickname}"

class Travel(models.Model):
    destination = models.CharField(max_length=250)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    traveler = models.ManyToManyField(User, related_name='travels')
    # travelers
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()
    
    def __str__(self):
        return f"{self.destination}"
    def __repr__(self):
        return f"{self.destination}"
