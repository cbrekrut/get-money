from django.db import models

class Data(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    task = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.date)