from django.db import models
from .position import Position
class Task(models.Model):
    code = models.CharField(max_length=50)
    name = models.TextField()
    count_times = models.FloatField(default=0)
    count_detail = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sels = models.IntegerField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


    def __str__(self):
        return self.name