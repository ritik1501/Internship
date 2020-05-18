from django.db import models

# Create your models here.
class UserData(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    fever = models.IntegerField()
    cough = models.IntegerField()
    throat = models.IntegerField()
    breathing = models.IntegerField()
    result = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'User name '+ self.name