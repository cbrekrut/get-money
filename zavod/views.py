from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from openpyxl import Workbook
from django.views.decorators.http import require_POST
import json
from .models import Employee, Position, Task, Data
from .forms import UploadFileForm
import pandas as pd

def employee_list(request):
    employees = Employee.objects.all()
    positions = Position.objects.all()
    tasks = Task.objects.all()
    return render(request, 'zavod/employee_list.html', {'employees': employees, 'positions': positions, 'tasks': tasks})


def generate_excel(request):
    # Get data from the database
    data_objects = Data.objects.all()

    # Create a new workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Write column headers
    headers = ['Full Name', 'Position', 'Task', 'Date']
    for col_num, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Write data rows
    for row_num, data_object in enumerate(data_objects, 2):
        worksheet.cell(row=row_num, column=1, value=data_object.full_name)
        worksheet.cell(row=row_num, column=2, value=data_object.position)
        worksheet.cell(row=row_num, column=3, value=data_object.task)
        worksheet.cell(row=row_num, column=4, value=data_object.date.strftime('%Y-%m-%d'))

    # Create the response with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employee_data.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response

@require_POST
def save_data(request):
    data = json.loads(request.body)
    fio = data.get('fio')
    position = data.get('position')
    tasks = data.get('tasks', [])
    tasks_count = data.get('tasks_count',[])
    index = 0
    for task_description in tasks:
        for i in range(int(tasks_count[index])):
            task_instance = Data(full_name = fio,position = position,task = task_description)
            task_instance.save()
        index+=1

    return JsonResponse({'message': 'Data saved successfully'})

def reports(request):
    return render(request,'zavod/reports.html')

def orders(request):
    return render(request,'zavod/orders.html')



def upload_orders(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            file = request.FILES['file']
            df = pd.read_excel(file)    
            
            for index, row in df.iterrows():
                description = row['Task']
                cost = row['Cost']
                Task.objects.create(description=description, cost=cost)

            return redirect('orders')  # Redirect to the orders page after processing the file
    else:
        form = UploadFileForm()

    return render(request, 'zavod/upload_orders.html', {'form': form})
