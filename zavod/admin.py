from django.contrib import admin
from .models import Position, Employee, Task,Data

class DataAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'task', 'count', 'date', 'cost', 'status')
    list_filter = ('status',)  # Добавляем фильтр по полю status
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name','contacts','position','price')
admin.site.register(Data, DataAdmin)
admin.site.register(Position)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Task)

