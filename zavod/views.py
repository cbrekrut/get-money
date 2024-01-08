from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from openpyxl import Workbook
from django.views.decorators.http import require_POST
import json
from .models import Employee, Position, Task, Data
from .forms import UploadFileForm
import pandas as pd
from datetime import datetime
from django.contrib.auth.decorators import login_required


def employee_list(request):
    employees = Employee.objects.all()
    positions = Position.objects.all()
    tasks = Task.objects.all()
    return render(request, 'zavod/employee_list.html', {'employees': employees, 'positions': positions, 'tasks': tasks})

def get_tasks(request):
    selected_position = request.GET.get('position')
    tasks = Task.objects.filter(position__title=selected_position).values('name')
    return JsonResponse(list(tasks), safe=False)


def generate_excel(request):
    # Check if the form is submitted
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Filter data based on the date range
        data_objects = Data.objects.filter(date__range=(start_date, end_date),status='approved')
    else:
        # If the form is not submitted, get all data
        data_objects = Data.objects.all()

    # Create a new workbook and add a worksheet
    workbook = Workbook()
    worksheet = workbook.active

    # Write column headers
    headers = ['Full Name', 'Position', 'Task', 'Date', 'Cost', 'Count', 'Money']
    for col_num, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col_num, value=header)

    # Write data rows
    for row_num, data_object in enumerate(data_objects, 2):
        worksheet.cell(row=row_num, column=1, value=data_object.full_name)
        worksheet.cell(row=row_num, column=2, value=data_object.position)
        worksheet.cell(row=row_num, column=3, value=data_object.task)
        worksheet.cell(row=row_num, column=4, value=data_object.date.strftime('%Y-%m-%d'))
        worksheet.cell(row=row_num, column=5, value=data_object.cost)
        worksheet.cell(row=row_num, column=6, value=data_object.count)
        worksheet.cell(row=row_num, column=7, value=(int(data_object.count) * int(data_object.cost)))

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
    tasks_count = data.get('tasks_count', [])

    for i, task_description in enumerate(tasks):
        task_count = int(tasks_count[i])

        # Находим соответствующий объект Task по описанию
        task_instance = Task.objects.get(name=task_description)

        # Проверяем, чтобы count не стал отрицательным
        if task_instance.count_detail >= task_count:
            task_instance.count_detail -= task_count
            task_instance.save()
            data_instance = Data(full_name=fio, position=position, task=task_description, count=task_count,cost = task_instance.cost)
            data_instance.save()
            return JsonResponse({'message': 'Data saved successfully'})
      
        

    return JsonResponse({'message': 'Data Failed'})

@login_required
def reports(request):
    employees = Employee.objects.all()
    return render(request,'zavod/reports.html',{'employees': employees})

@login_required
def orders(request):
    active_orders = Task.objects.filter(count_detail__gt=0)
    context = {'active_orders': active_orders}
    return render(request, 'zavod/orders.html', context)


@login_required
def upload_orders(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                code = row['Task Code'] 
                name = row['Task']
                count_times = float(row['Count Times'])
                count_detail = int(row['Count Detail'])
                cost = row['Cost']
                sels = int(row['Sales'])
                position_title = row['Position']  

                position = get_object_or_404(Position, title=position_title)
                Task.objects.create(
                    code=code,
                    name=name,
                    count_times=count_times,
                    count_detail=count_detail,
                    cost=cost,
                    sels=sels,
                    position=position
                )

            return redirect('orders')  # Перенаправляем на страницу заказов после обработки файла

    else:
        form = UploadFileForm()

    return render(request, 'zavod/upload_orders.html', {'form': form})

def workshop_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        workshop = request.POST.get('workshop')

        # Fetch tasks based on the provided filters
        filtered_tasks = Data.objects.filter(
            date__range=[start_date, end_date],
            position=workshop
        )

        wb = Workbook()
        ws = wb.active

        headers = ['Workshop', 'Full Name', 'Order Number']
        ws.append(headers)

        for task in filtered_tasks:
            row_data = [task.position, task.full_name, task.count]
            ws.append(row_data)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=workshop_report_{start_date}_{end_date}.xlsx'
        wb.save(response)

    return response

def generate_employee_report_excel(employee, employee_data):
    wb = Workbook()
    ws = wb.active

    ws.append(['Name','Date', 'Task', 'Count', 'Cost'])
    for data in employee_data:
        ws.append([data.full_name, data.date, data.task, data.count, data.cost])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="employee_report.xlsx'

    wb.save(response)

    return response

def employee_report(request):
    if request.method == 'POST':
        employee = request.POST.get('employee')
        start_date_employee = request.POST.get('start_date_employee')
        end_date_employee = request.POST.get('end_date_employee')

        start_date_employee = datetime.strptime(start_date_employee, '%Y-%m-%d').date()
        end_date_employee = datetime.strptime(end_date_employee, '%Y-%m-%d').date()
        
        employee_data = Data.objects.filter(full_name=employee, date__range=(start_date_employee, end_date_employee))

        if not employee_data.exists():
            return HttpResponse("No data available for the selected employee and date range.")

        return generate_employee_report_excel(employee, employee_data)

    return HttpResponse("Invalid request method.")
