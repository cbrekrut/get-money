from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    contacts = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.full_name
