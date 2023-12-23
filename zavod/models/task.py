from django.db import models

class Task(models.Model):
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    def __str__(self):
        return self.description