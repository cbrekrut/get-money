from django.db import models
from django.utils import timezone
class Data(models.Model):
    full_name = models.CharField(max_length=100)
    code = models.CharField(max_length=100,default='0')
    position = models.CharField(max_length=50)
    task = models.CharField(max_length=100)
    count = models.IntegerField()
    date = models.DateField("date",editable=True,default=timezone.now)
    cost = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('moderation', 'На модерации'), ('approved', 'Одобрена')],
        default='moderation'
    )
    def __str__(self):
        return str((self.date)) +' '+ str(self.status)