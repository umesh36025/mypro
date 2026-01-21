from django.shortcuts import render
from datetime import datetime,date,time,timedelta
from datetime import date
from accounts.RequiredImports import *
from .models import *
from task_management.filters import get_taskStatus_object

def get_financial_year_details():
    input_date = date.today()
    year = input_date.year
    month = input_date.month
    day=input_date.day
    
    if month >= 4:
        financial_year = f"{year}-{year + 1}"
    else:
        financial_year = f"{year - 1}-{year}"

    if month in (4, 5, 6):
        quarter = "Q1"
    elif month in (7, 8, 9):
        quarter = "Q2"
    elif month in (10, 11, 12):
        quarter = "Q3"
    else:
        quarter = "Q4"

    quarter_months = {
        "Q1": {4:"April", 5:"May", 6:"June"},
        "Q2": {7:"July", 8:"August", 9:"September"},
        "Q3": {10:"October", 11:"November", 12:"December"},
        "Q4": {1:"January", 2:"February", 3:"March"},
    }
    
    reversed_quater_month= {
        "Q1": {"April":1, "May":2, "June":3},
        "Q2": {"July":1, "August":2, "September":3},
        "Q3": {"October":1, "November":2,"December":3},
        "Q4": {"January":1, "February":2, "March":3},
    }
    quarter_month=quarter_months[quarter][month]
    quarter_month_reversed=reversed_quater_month[quarter][quarter_month]
    print(quarter_month,quarter_month_reversed)

    return {
        "financial_year": financial_year,
        "quarter": quarter,
        "respective_quarter_months": quarter_month,
        "reverse_quater_month":quarter_month_reversed
    }

def get_addeded_entries_by_username_Date(request:HttpRequest,date=None,username=None):
        try:
            user_obj=get_object_or_404(User,username=username)
            # Role-based filtering
            if user_obj and date:
                entries = UsersEntries.objects.select_related("user", "month_and_quater_id","status").filter(user=user_obj,date=date).order_by("date")
            
            elif user_obj and not date:
                entries = UsersEntries.objects.select_related("user", "month_and_quater_id","status").filter(user=user_obj).order_by("date")
                
            else:
                return JsonResponse({"error": "invalid query parameter"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                
            data = []
            for entry in entries:
                data.append({
                    "id":entry.id,
                    "note":entry.note,
                    "meeting_head": entry.month_and_quater_id.Meeting_head,
                    "meeting_sub_head": entry.month_and_quater_id.meeting_sub_head,
                    "username": entry.user.username,
                    "date": entry.date,
                    "status": entry.status.status_name,
                    "month_quater_id": entry.month_and_quater_id.quater.quater,
                })
            return data
        except Http404 as e:
            print(e)
            return JsonResponse({"error": "User profile not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)
            ...
            
def get_meeting_head_and_subhead(request:HttpRequest,user_id:str):
    verify_method=verifyGet(request)
    if verify_method:
        return verify_method
    try:
        user=get_object_or_404(User,username=user_id)
        user_profile=get_object_or_404(Profile,Employee_id=user)
        get_quater_data=get_financial_year_details()
        quater=get_quater_data.get("quarter")
        quarter_obj=get_object_or_404(Quaters,quater=quater)
        actual_month=get_quater_data.get("respective_quarter_months")
        department_obj=user_profile.Department
        financial_year=get_quater_data.get("financial_year")
        reverse_month=get_quater_data.get("reverse_quater_month")
        print(get_quater_data)
    except Http404 as e:
        print(e)
        return JsonResponse({"Message":"http occured"})
    except Exception as e:
        print(e)
        return JsonResponse({"Message":"Error occured"}) 
    else:
        get_monthly_schedule_set=Monthly_department_head_and_subhead.objects.filter(month_of_the_quater=reverse_month,quater=quarter_obj,
                                                                        department=department_obj)
        values=[{"quater":obj.quater.quater,
                "financial_year":financial_year,
                "month":reverse_month,
                "actual_month":actual_month,
                "Meeting-head":obj.Meeting_head,
                "Sub-Meeting-head":obj.meeting_sub_head,
                "sub-head-D1":obj.Sub_Head_D1,
                "sub-head-D2":obj.Sub_Head_D2,
                "sub-head-D3":obj.Sub_Head_D3 
                } for obj in get_monthly_schedule_set]
        
        return JsonResponse(values,safe=False)
    ...

@csrf_exempt
@login_required
def create_multiple_user_entries(request):
    verify_method=verifyPost(request)
    if verify_method:
        return verify_method
    try:
        fields=["date","entries","month_quater_id"]
        data = load_data(request)
        entry_date = data.get("date")
        month_quater_id = data.get("month_quater_id")
        entries = data.get("entries")
        if not all(fields):
            return JsonResponse({"error": "Invalid payload"}, status=400)
        user = request.user
        created_entries = []
        for entry in entries:
            note=entry.get("note")
            status=entry.get("status")
            
            if not note or not status:
                continue

            status_obj=get_taskStatus_object(status_name=status)
            month_quater = Monthly_department_head_and_subhead.objects.get(id=month_quater_id)

            obj = UsersEntries.objects.create(
                status=status_obj,
                user=user,
                month_and_quater_id=month_quater,
                date=entry_date,
                note=note
            )
            created_entries.append(obj.id)
        print(created_entries)
        return JsonResponse({
            "message": "Entries created successfully",
            "created_entry_ids": created_entries
        }, safe=False,status=201)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found, pass the correct username"}, status=404)
    
    except TaskStatus.DoesNotExist:
        return JsonResponse({"error": "Incorrect Status passed in the body"}, status=404)

    except Monthly_department_head_and_subhead.DoesNotExist:
        return JsonResponse({"error": "Invalid month_quater_id"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def get_entries(request: HttpRequest):
    verify_method=verifyGet(request)
    if verify_method:
        return verify_method
    try:
        login_users_username=request.user.username
        data=request.GET
        username=data.get("username")
        date=data.get("Date")
        superuser=request.user.is_superuser
        if username and superuser and date:
            data=get_addeded_entries_by_username_Date(request,date=date,username=username)

        elif username and superuser and not date:
            data=get_addeded_entries_by_username_Date(request,username=username)
            
        elif username==login_users_username and not superuser and date:
            data=get_addeded_entries_by_username_Date(request,username=username,date=date)
                
        elif username==login_users_username and not superuser and not date:
            data=get_addeded_entries_by_username_Date(request,username=username)
        else:
                raise PermissionDenied("Not authorised")

    except PermissionDenied as e:
            print(e)
            return JsonResponse({"message":"you are not authorised to access other users records"},status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)
    else:
        if isinstance(data,JsonResponse):
            return data
        return JsonResponse(data,safe=False,status=200)

@login_required
@csrf_exempt
def change_status(request: HttpRequest,user_entry_id:int):
    request_method=verifyPatch(request)
    if request_method:
        return request_method
    data=load_data(request)
    changed_to:str=data.get("change_Status_to")
    try:
        user_entry=UsersEntries.objects.get(id=user_entry_id)
        changed_status=get_taskStatus_object(status_name=changed_to.upper())
        setattr(user_entry,"status",changed_status)
        user_entry.save()
    except Exception as e:
        return JsonResponse({"message":f"{e}"})
    else:
        return JsonResponse({"message":f"Status Changed to {changed_to}"})
# Create your views here.

@csrf_exempt       
def add_meeting_head_subhead(request:HttpRequest):
    data=load_data(request)
    quater=data.get("quater")
    month=data.get("month")
    head=data.get("head")
    sub_head=data.get("sub_head")
    sub_d1=data.get("sub_d1")
    sub_d2=data.get("sub_d2")
    sub_d3=data.get("sub_d3")
    try:
        department=get_department_obj(dept=data.get("dept"))
        quater_object=Quaters.objects.get(quater=quater)
    except Exception as e:
        print(e)
        return JsonResponse({"Message":"Error occured"})
    else:
        Monthly_department_head_and_subhead.create_head_and_subhead_for_each_dept(dept=department,quater=quater_object,
                                                                            month_of_the_quater=month,Meeting_head=head,meeting_sub_head=sub_head,
                                                                            Sub_Head_D1=sub_d1,Sub_Head_D2=sub_d2,Sub_Head_D3=sub_d3)
    
    return JsonResponse({"Message":"added successfully"})