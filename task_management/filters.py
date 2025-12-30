from django.http import HttpRequest, JsonResponse

from accounts.models import Profile, Roles
from django.db.models import Q

from task_management.models import TaskTypes,Task


def get_available_roles(request: HttpRequest):
    profile=Profile.objects.get(Employee_id=request.user)
    if request.GET:
        role=request.GET.get("role")
    else:
        role=profile.Role
    if role=="MD":
        roles=Roles.objects.filter().values("role_name")
        return JsonResponse(list(roles),safe=False,status=200)
    elif role=="TeamLead":
        roles=Roles.objects.exclude(Q(role_name="MD") | Q(role_name="Admin")).values("role_name")
        return JsonResponse(list(roles),safe=False,status=200)
    elif role=="Employee":
        roles=Roles.objects.exclude(Q(role_name="MD") | Q(role_name="Admin")).values("role_name")
        return JsonResponse(list(roles),safe=False,status=200)
    elif role=="Intern":
        roles=Roles.objects.exclude(Q(role_name="MD") | Q(role_name="Admin")).values("role_name")
        return JsonResponse(list(roles),safe=False,status=200)
    else:
        roles=[{}]
        return JsonResponse(list(roles),safe=False,status=200)
    
def get_usernames_from_selected_role_and_desigantion(request: HttpRequest):

   designation=request.GET.get("designation")
   role=request.GET.get("role")
   try:
    # if not user
    if not request.user:
        return JsonResponse({"error": "login required"}, status=404)
    # for md
    elif not role and not designation:
        names=Profile.objects.filter().values("Name")
    elif not role:
        names=Profile.objects.filter(Designation=designation).values("Name")
    elif not designation:
        names=Profile.objects.filter(Role=role).values("Name")
    elif role=="MD" and not designation:
        names=Profile.objects.filter(Role="MD").values("Name")
    elif role=="MD" and designation:
        names=Profile.objects.filter(Role="MD",Designation=designation).values("Name")
    # for team lead
    elif role=="TeamLead" and  not designation:
        names=Profile.objects.exclude(Q(Role="MD") | Q(Role="Admin")).values("Name")
    elif role=="TeamLead" and  designation:
        names=Profile.objects.filter(Q(Role="Intern") | Q(Role="Employee") | Q(Role="TeamLead"),Designation=designation).values("Name")
    # for employees
    elif role=="Employee" and  not designation:
        names=Profile.objects.exclude(Role="MD").values("Name")
    elif role=="Employee" and  designation:
        names=Profile.objects.filter(Q(Role="Employee") | Q(Role="Intern") | Q(Role="TeamLeader"),Designation=designation).values("Name")
    # for interns
    elif role=="Intern" and  not designation:
        names=Profile.objects.exclude(Q(Role="MD") | Q(Role="admin")).values("Name")
    elif role=="Intern" and  designation:
        names=Profile.objects.filter(Q(Role="Employee") | Q(Role="Intern") | Q(Role="TeamLEad"),Designation=designation).values("Name")
    else:
        return JsonResponse({"message":"Choose the correct designation"}, status=302)
    
   except Exception as e:
       return JsonResponse({"message":f"{e}"}, status=302)
   else:
        return JsonResponse(list(names), status=200,safe=False)
    
def get_types(request: HttpRequest):
    task_types=TaskTypes.objects.all().values("type_name")
    return JsonResponse(list(task_types),safe=False)

def get_tasks_by_type(request: HttpRequest,type:str):
    if type.lower()=="all":
        tasks=Task.objects.filter(assigned_to=request.user,created_by=request.user).select_related("type","status").values()
    else:
        task_type=TaskTypes.objects.get(type_name=type)
        tasks=Task.objects.filter(type=task_type,assigned_to=request.user,created_by=request.user).select_related("type","status").values()
    
    return JsonResponse(list(tasks),safe=False)

        
        
    