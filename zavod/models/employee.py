from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10, default = '1')

    def __str__(self):
        return self.full_name