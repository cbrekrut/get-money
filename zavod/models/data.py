from django.db import models

class Data(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    task = models.CharField(max_length=100)
    count = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    cost = models.IntegerField()
    def __str__(self):
        return str(self.date)