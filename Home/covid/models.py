from django.db import models
from datetime import datetime   

# Create your models here.
class UserData(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    fever = models.IntegerField()
    cough = models.IntegerField()
    throat = models.IntegerField()
    breathing = models.IntegerField()
    result = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return 'User name '+ self.name

class LargeData(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.IntegerField()
    fever = models.IntegerField()
    cough = models.IntegerField()
    throat = models.IntegerField()
    weakness = models.IntegerField()
    diffBreath = models.IntegerField()
    drowsiness = models.IntegerField()
    pain = models.IntegerField()
    travel = models.IntegerField()
    symptoms = models.IntegerField()
    blood = models.IntegerField()
    appetide = models.IntegerField()
    result = models.IntegerField()
    timestamp = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return 'User name '+ self.name