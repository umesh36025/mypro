from django.http import HttpRequest, JsonResponse
from django.views import View
from accounts.models import Designation,Roles,Profile,User,Branch
from django.db import models

def get_user_role(user:User):
    try:
        profile=Profile.objects.get(Employee_id=user)
    except Exception as e:
        return {"message":f"{e}"}
    else:
        return profile.Role
        
def get_designations(request:HttpRequest):
    role=get_user_role(request.user)
    if role == "MD":
        designations=[{}]
    else:
        designations=Designation.objects.all().values("designation")
    return JsonResponse(list(designations),safe=False)

def get_roles(request: HttpRequest):
    roles=Roles.objects.all().values("role_name")
    return JsonResponse(list(roles),safe=False)

def get_branches(request: HttpRequest):
    role=get_user_role(request.user)
    if role=="MD":
        branch=[{}]
    else:
        branch=Branch.objects.all().values("branch_name")
    return JsonResponse(list(branch),safe=False)

def get_designations_by_branch(request: HttpRequest):
    ...