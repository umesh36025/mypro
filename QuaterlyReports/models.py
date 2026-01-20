from django.db import models
from accounts.models import *
from task_management.models import TaskStatus

class Quaters(models.Model):
    quater=models.CharField(max_length=20,null=False,primary_key=True)
    start_month=models.IntegerField(null=True)
    end_month=models.IntegerField(null=True)
    
    @classmethod
    def create_quater(cls,quater:str,starting_month:int,ending_month:int):
        obj=cls.objects.create(quater=quater,start_month=starting_month,end_month=ending_month)
        return obj
    
    class Meta:
        db_table= 'team_management"."Quaters'
        verbose_name_plural = "quaters"
        ordering=["quater"]
    
class Monthly_department_head_and_subhead(models.Model):
    department=models.ForeignKey(Departments,on_delete=models.CASCADE,null=False,related_name="dapartment",db_column="department")
    quater=models.ForeignKey(Quaters,on_delete=models.CASCADE,null=False,related_name="meeting_head_quater")
    month_of_the_quater=models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    Meeting_head=models.CharField(max_length=100,null=False)
    meeting_sub_head=models.CharField(max_length=100,null=True)
    Sub_Head_D1=models.CharField(max_length=100,null=True)
    Sub_Head_D2=models.CharField(max_length=100,null=True)
    Sub_Head_D3=models.CharField(max_length=100,null=True)
    
    
    @classmethod
    def create_head_and_subhead_for_each_dept(cls,quater:Quaters,dept:Departments,month_of_the_quater:int,
                                            Meeting_head:str,meeting_sub_head:str,Sub_Head_D1:str,
                                            Sub_Head_D2:str,Sub_Head_D3:str):
        
        obj=cls.objects.create(quater=quater,department=dept,month_of_the_quater=month_of_the_quater,
                            Meeting_head=Meeting_head,Sub_Head_D1=Sub_Head_D1,Sub_Head_D2=Sub_Head_D2,
                            Sub_Head_D3=Sub_Head_D3,meeting_sub_head=meeting_sub_head)
        return obj
    
    class Meta:
        db_table= 'team_management"."Monthly_department_wise_head_and_subhead'
        ...

class UsersEntries(models.Model):
    month_and_quater_id=models.ForeignKey(Monthly_department_head_and_subhead,on_delete=models.CASCADE,db_column="month_quater",null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field="username",db_column="Employee_id",null=False)
    date=models.DateField(auto_now=False,auto_now_add=False)
    status=models.ForeignKey(TaskStatus,editable=True,null=False,on_delete=models.CASCADE)
    note=models.TextField(null=False)
    
    class Meta:
        db_table= 'team_management"."UserEntries'

# Create your models here.
