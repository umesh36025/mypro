from django.http import HttpRequest, HttpResponse, JsonResponse
from accounts.models import Profile, Roles,Designation
from django.db.models import Q,F
from accounts.views import status
from task_management.models import *
from accounts.filters import get_role_object,get_designation_object

# # # # # #  baseurl="http://localhost:8000" # # # # # # # # # # # # 
    
# get a "Task" object from task_id
def get_task_object(task_id:int):
    try:
        task=Task.objects.get(task_id=task_id)
    except Exception as e:
        print(e)
        return None
    else:
        return task
    
# get a "TaskType" object from type_name
def get_taskTypes_object(type_name:str):
    try:
        type=TaskTypes.objects.get(type_name=type_name)
    except Exception as e:
        print(e)
        return None
    else:
        return type
    
# get a "TaskStatus" object from status_name
def get_taskStatus_object(status_name:str):
    try:
        status_object=TaskStatus.objects.get(status_name=status_name)
    except Exception as e:
        print(e)
        return None
    else:
        return status_object
        
# get Employees Name list from specified desigantion and role.
# endpoint-{{baseurl}}/tasks/getNamesfromRoleandDesignation/
# Use in the dropdown of fiels "Assigned_to" while assigning/ creating tasks.
def get_Names_from_selected_role_and_desigantion(request: HttpRequest):
   designation=request.GET.get("designation")
   role=request.GET.get("role")
   try:
    # if not user
    if not request.user:
        return JsonResponse({"error": "login required"}, status=404)
    elif not role and not designation:
        names=Profile.objects.all().order_by("Name").values("Name")
    elif role and not designation:
        passed_role=get_role_object(role=role)
        names=Profile.objects.filter(Role=passed_role).order_by("Name").values("Name")
    elif designation and not role:
        passed_designation=get_designation_object(designation=designation)
        names=Profile.objects.filter(Designation=passed_designation).order_by("Name").values("Name")
    elif role and designation:
        passed_role=get_role_object(role=role)
        passed_designation=get_designation_object(designation=designation)
        names=Profile.objects.filter(Role=passed_role,Designation=passed_designation).order_by("Name").values("Name")
    else:
        return JsonResponse({"message":"pass the correct designation or Role to filter names"}, status=status.HTTP_404_NOT_FOUND)
   except Exception as e:
       return JsonResponse({"message":f"{e}"}, status=status.HTTP_404_NOT_FOUND)
   else:
        return JsonResponse(list(names), status=status.HTTP_200_OK,safe=False)

# Get all the types of task that can be assingnable.
# endpoint-{{baseurl}}/tasks/getTaskTypes/
# Use in the dropdown of TaskTypes while creating a task
def get_types(request: HttpRequest):
    task_types=TaskTypes.objects.all().values("type_name")
    return JsonResponse(list(task_types),safe=False)

# Fetch tasks by its types
# endpoint for "Created_Tasks"-{{baseurl}}/tasks/viewTasks/?type= 
# endpoint for "Assigned_Reported"-{{baseurl}}/tasks/viewAssignedTasks/?type= 
def get_tasks_by_type(request:HttpRequest,type:str="all",self_created: bool=True):
    if type.lower()=="all" and not self_created:
        tasks=Task.objects.filter(assigned_to=request.user).select_related("type","status","created_by").annotate(task_type=F("type__type_name"),
            current_status=F("status__status_name"),created=F("created_by__accounts_profile__Name")).order_by("-task_id").values("task_id","title","description","due_date",
                    "task_type","created","current_status")
        return list(tasks)
    
    elif type.lower()=="all" and self_created:
        tasks=Task.objects.filter(created_by=request.user).select_related("type","status","assigned_to").annotate(task_type=F("type__type_name"),
            current_status=F("status__status_name"),assigned=F("assigned_to__accounts_profile__Name")).order_by("-task_id").values("task_id","title","description","due_date",
                    "task_type","assigned","current_status")
        return list(tasks)
    
    elif type and not self_created:
        type_obj=TaskTypes.objects.get(type_name=type)
        tasks=Task.objects.filter(type=type_obj,assigned_to=request.user).select_related("type","status","created_by").annotate(task_type=F("type__type_name"),
            current_status=F("status__status_name"),created=F("created_by__accounts_profile__Name")).order_by("-task_id").values("task_id","title","description","due_date",
                    "task_type","created","current_status")
        return list(tasks)
    
    elif type and self_created:
        type_obj=TaskTypes.objects.get(type_name=type)
        tasks=Task.objects.filter(type=type_obj,created_by=request.user).select_related("type","status","assigned_to").annotate(task_type=F("type__type_name"),
            current_status=F("status__status_name"),assigned=F("assigned_to__accounts_profile__Name")).order_by("-task_id").values("task_id","title","description","due_date",
                    "task_type","assigned","current_status")
        return list(tasks)

    else:
        tasks=[{"message":"Incorrect type for tasks"}]
    return tasks