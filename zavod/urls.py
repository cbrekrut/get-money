from django.urls import path
from . import views 

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('save-data/', views.save_data, name='save_data'),
    path('generate-excel/', views.generate_excel, name='generate_excel'),
    path('reports/',views.reports, name='reports'),
    path('orders/',views.orders, name='orders'),
    path('upload_orders/', views.upload_orders, name='upload_orders'),
    path('workshop_report/', views.workshop_report, name='workshop_report'),
    path('get-tasks/', views.get_tasks, name='get_tasks'),
]
