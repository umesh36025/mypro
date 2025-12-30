# from django.contrib.auth.hashers import get_hasher
from accounts.filters import *
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .models import Profile,User,Roles,Designation
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
import os
from settings import BASE_DIR
from rest_framework import status
from django.http.response import JsonResponse
from .snippet import admin_required

def home(request: HttpRequest):
    # return JsonResponse({"messege":"You are at Accounts section"})
    # return redirect("/accounts/login")
    # return redirect("login")
    return HttpResponse(status=204)

@csrf_exempt
@admin_required
def create_employee_login(request: HttpRequest):
    fields=['Employee_id','password','Name','Role','Email_id','Designation','Date_of_join','Date_of_birth','Branch','Photo_link']
    login_values={}
    profile_values={}
    try:
        if request.method == "POST":
            # For 'json' content type
            if request.content_type=="application/json":
                # ...
                data=json.loads(request.body)
                for i in fields:
                    field_value=data.get(i)
                    if not field_value:
                        return JsonResponse({"messege":f"{i} is required"},status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif i=='Employee_id':
                        login_values["username"]=field_value
                    elif i=='password':
                        login_values[i]=field_value
                    elif i == 'Email_id':
                        login_values[i]=field_value
                        profile_values[i]=field_value
                    else:
                        profile_values[i]=field_value

        # for other types of request content types
            else:
                data=request.POST
                files=request.FILES
                for i in fields:
                    if i!="Photo_link":
                        field_value=data.get(i)
                    else:
                        field_value=files.get(i)
                    if not field_value:
                        return JsonResponse({"messege":f"{i} is required"},status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif i=='Employee_id':
                        login_values["username"]=field_value
                    elif i=='password':
                        login_values[i]=field_value
                    elif i == 'Email_id':
                        login_values["email"]=field_value
                        profile_values[i]=field_value
                    else:
                        profile_values[i]=field_value
        else:
            return JsonResponse({"messege":"create employee login credentials here"},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({"messege":f"{e}"},status=status.HTTP_206_PARTIAL_CONTENT)
    else:
        try:
            user = User.objects.create(**login_values )
            user.set_password(login_values["password"])
            user.save()
        except Exception as e:
            return JsonResponse({"messege":f"{e}"})
        else:
            try:
                profile_values["Employee_id"]=user
                user_profile=Profile.objects.create(**profile_values)
                user_profile.save()
            
            # return HttpJsonResponse(content="Employee created successfully")
                return JsonResponse({"messege":"Employee Created successfully"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"messege":f"{e}"})
            
@login_required
def get_all_employees(request: HttpRequest):
    profile=Profile.objects.filter(Employee_id=request.user).first()
    if request.user.is_superuser or profile.Role=="MD":
        profile_data=Profile.objects.filter().values("Employee_id","Email_id","Designation","Date_of_birth","Date_of_join","Branch","Name","Photo_link","Role") 
        return  JsonResponse(list(profile_data),safe=False)
    else:
        return JsonResponse({"message":"Unauthorised access"},status=404)
    

@admin_required
def get_session_data(request: HttpRequest):
    if not request.user:
        return JsonResponse({"messege":"login credentials required"},status=status.HTTP_200_OK)
    else:
        session_data={}
        session_data["expiray-age"]=request.session.get_expiry_age()
        session_data["expiray-date"]=request.session.get_expiry_date()
        session_data["accessed"]=request.session.accessed
        session_data["is_empty"]=request.session.is_empty()
        return JsonResponse(session_data)
            
@csrf_exempt
def user_login(request:HttpRequest):
    # request content type is in json format
    if request.method == "POST":
        if request.content_type=="application/json":
            data=json.loads(request.body)
            u = data.get('username')
            p = data.get('password')
        
    # for other types of body content 
        else:
            data=request.POST
            u=data.get('username')
            p=data.get('password')
            
    else:
        return  JsonResponse({"messege":"Login Here"},status=status.HTTP_200_OK)
    
    user= authenticate(request,username=u,password=p)
        
    if not user:
            return  JsonResponse({"messege":"Incorrect userID/Password"})
    else:
            login(request,user)
            if not user.is_superuser:                
                profile=Profile.objects.get(Employee_id=user)
                return  JsonResponse({"messege":"You are logged in","username":f"{request.user.username}","Role":getattr(profile,"Role",None)})
            else:
                return  JsonResponse({"messege":"You are logged in","username":f"{request.user.username}","Role":"Admin"},status=status.HTTP_202_ACCEPTED)

@login_required
def employee_dashboard(request: HttpRequest):
    if request.user.is_superuser:
        return  JsonResponse({"messege":"This is a Admin information dashboard","username":f"{request.user.username}"})
        # print(profile)
        # return HttpResponse()
    else:
        profile=Profile.objects.filter(Employee_id=request.user).values("Employee_id","Email_id","Designation","Date_of_birth","Date_of_join","Branch","Name","Photo_link","Role")
        
    return  JsonResponse(list(profile),safe=False)

@login_required
def user_logout(request: HttpRequest):
    logout(request)
    request.session.flush()
    return  JsonResponse({"messege":"Logout successfully"},status=status.HTTP_200_OK)
    
@csrf_exempt
@admin_required
def update_profile(request: HttpRequest,username):
    if request.method in ['PUT','PATCH','POST']:
        fields=['password','Name','Role','Email_id','Designation','Date_of_join','Date_of_birth','Branch','Photo_link']
        login_values={}
        profile_values={}
            # if request.content_type=="application/json":
            #     data=json.loads(request.body)
            #     for i in fields:
            #         field_value=data.get(i)
            #         if not field_value:
            #             return JsonResponse({"messege":f"{i} is empty"},status=status.HTTP_406_NOT_ACCEPTABLE)
            #         elif i=='password' :
            #             login_values[i]=field_value
            #         elif i == 'Email_id':
            #             login_values[i]=field_value
            #             profile_values[i]=profile_values
            #         else:
            #             profile_values[i]=field_value
        # for other types of body content 
        try:
            
                data=request.POST
                files=request.FILES
                for i in fields:
                    if i!= "Photo_link":
                        field_value=data.get(i)
                    else:
                        field_value=files.get(i)
                    if not field_value:
                        return JsonResponse({"messege":f"{i} is empty"},status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif i=='password':
                        login_values[i]=field_value
                    elif i == 'Email_id':
                        login_values["email"]=field_value
                        profile_values[i]=field_value
                    else:
                        profile_values[i]=field_value
            
        except Exception as e:
            return  JsonResponse({"messege":f"{e}"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        else:
            try:
                user=User.objects.get(username=username)
                profile=Profile.objects.get(Employee_id=user)
            except Exception as e:
                return  JsonResponse({"messege":f"{e}"},status=status.HTTP_404_NOT_FOUND) 
        try:    
            setattr(user,'password',login_values['password'])
            setattr(user,'email',login_values['email'])
            user.set_password(login_values['password'])
            user.save()
            if profile.Photo_link:
                profile.Photo_link.delete(save=True)
        except Exception as e:
            return  JsonResponse({"messege":f"{e}"})
        else:
            uddated_profile=Profile.objects.filter(Employee_id=user).update(**profile_values)
            return  JsonResponse({"messege":"user details update successfully"},status=status.HTTP_205_RESET_CONTENT)
    else:
        return  JsonResponse({"messege":"update users here"},status=status.HTTP_200_OK)
            # ...
# Individual Employee Dashboard View
@login_required
@admin_required
def view_employee(request: HttpRequest,u):
    user=User.objects.get(username=u)
    profile=Profile.objects.filter(Employee_id=user).values("Employee_id","Email_id","Designation","Date_of_birth","Date_of_join","Branch","Name","Photo_link","Role")
    return JsonResponse(list(profile),safe=False)

@login_required
@admin_required
@csrf_exempt
def delete_user_profile(request: HttpRequest,u):
    if request.method=='DELETE':
        user=User.objects.get(username=u)
        # profile=Profile.objects.get(Employee_id=user)
    
        if user:
            user.delete()
            return JsonResponse({"message":"user deleted successfully"})
        else:
            return JsonResponse({"message":"user does not exist"})
    
    else:
            return JsonResponse({"message":"delete user"})
    
        