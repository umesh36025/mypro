from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from task_management.filters import *
from django.contrib.auth.models import User
from .models import *
from accounts.models import *
from django.db.models import Q
# from django.db.migrations import 
from django.http.request import HttpRequest
import json
from django.views.decorators.csrf import csrf_exempt 

def home(request: HttpRequest):
    if request.method == "GET":
        return JsonResponse({"message":"You are at tasks page"},status=200)
    else:
        return JsonResponse({"message":"Method is not allowed"},status=405)

@csrf_exempt
@login_required
def create_task(request:HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    user = request.user
    if not user:
        return JsonResponse({"error": "login required"}, status=405)
        
    if request.content_type=="application/json":
        data=json.loads(request.body)
    else:
        data=request.POST
        
    required_fields=["title","description","due_date","assigned_to","type"]
    body_data={}
    
    for i in required_fields:
        field_value=data.get(i)
        if not field_value:
            return JsonResponse({"error": f"{i} is required"}, status=302)
        body_data[i]=data.get(i)
    print(body_data)
        # print(request.user)
        # print(request.headers)
    try:
        task_type_id=TaskTypes.objects.get(type_name=body_data["type"])
        body_data["type"]=task_type_id
        u_profile= Profile.objects.get(Name=body_data["assigned_to"])
        body_data["assigned_to"]=u_profile.Employee_id
        body_data["created_by"]=request.user
    except Exception as e:
        return JsonResponse({"message":f"{e}"})
    else:
        try:
            task = Task.objects.create(**body_data)
            task.save()
            return JsonResponse({"message": "Task created"},status=201) 
        except Exception as e:
            return JsonResponse({"message":f"{e}"},status=302)
        
@csrf_exempt
@login_required
def update_task(request,task_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    user = request.user
    if not user:
        return JsonResponse({"error": "login required"}, status=405)
        
    if request.content_type=="application/json":
        data=json.loads(request.body)
    else:
        data=request.POST
        
    fields=["title","description","due_date","assigned_to","type"]
    body_data={}
    
    for i in fields:
        field_value=data.get(i)
        if field_value:
            # return JsonResponse({"error": f"{i} is required"}, status=302)
            body_data[i]=data.get(i)
        
    try:
        task_type_id=TaskTypes.objects.get(type_name=body_data["type"]).type_id
        body_data["type"]=task_type_id
        u_profile= Profile.objects.get(Name=body_data["assigned_to"])
        body_data["assigned_to"]=u_profile.Employee_id
    except Exception as e:
        return JsonResponse({"message":f"{e}"})
    try:
        # task = Task.objects.create(**body_data)
        task=Task.objects.filter(task_id=task_id).update(**body_data)
    except Exception as e:
        JsonResponse({"message":f"{e}"},status_code=302)
    else:
        return JsonResponse(
        {"message": "Task updated successfully"},
        status=201) 
    
    ...
    
@login_required
def show_created_tasks(request: HttpRequest):
    if request.method!="GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    if request.user.is_superuser:
        tasks=Task.objects.filter().select_related().values()
        return JsonResponse(list(tasks),safe=False,status=200)
        
    else:
        try:
            tasks=Task.objects.filter(created_by=request.user).select_related("status","type").values()
            # for task in tasks:
                # print(request.user)
            # return JsonResponse({"msg":"runs"})
        except Exception as e:
            return JsonResponse({"msg":f"{e}"})
        else:
            print(tasks)
            return JsonResponse(list(tasks),safe=False,status=200)
    
@login_required
def show_assigned_tasks(request: HttpRequest):
    if request.method!="GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    if request.user.is_superuser:
        tasks=Task.objects.filter(assigned_to=request.user).select_related("status","type").values()
        return JsonResponse(list(tasks),safe=False,status=200)
    
    try:
        tasks=Task.objects.filter(assigned_to=request.user).select_related().values()
    except Exception as e:
        return JsonResponse({"message":f"{e}"})
    else:
        return JsonResponse(list(tasks),safe=False,status=200)
        
@login_required
@csrf_exempt
def change_status(request: HttpRequest,task_id):
    if request.method != "PATCH":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    data=json.loads(request.body)
    changed_to=data.get("changed_status")
    
    task=Task.object.get(task_id=task_id)
    changed_to=TaskStatus.objects.get(status_name=changed_to).status_id
    setattr(task,"current_status",changed_to)
    task.save()
    
    return JsonResponse({"message":f"Status Changed to {changed_to}"})

def sort_tasks_by_date(request: HttpRequest):
    ...
    
def sort_tasks_by_type(request: HttpRequest):
    ...
    
def sort_tasks_by_status(request:HttpRequest):
    ...
    
def sort_tasks_by_Role(request: HttpRequest):
    ...
    
def sort_Tasks_by_designation(request: HttpRequest):
    ...
    
def sort_tasks_by_assigend_to(request: HttpRequest):
    ...
    
def sort_tasks_by_assigned_by(request: HttpRequest):
    ...
    
    
    

