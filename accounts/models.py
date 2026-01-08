from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser,AbstractBaseUser
from enum import Enum
from django.contrib.auth.models import User
from django.core.validators import validate_email

# class farm_emp_details(models.Model):
    # class Meta:
    #     db_table='team_farm"."farm_employee_details'
    #     verbose_name = "Farm Employee"
    #     verbose_name_plural = "Farm Employees"
            
    # Employee=models.OneToOneField(User, verbose_name="employee_id", on_delete=models.CASCADE,primary_key=True,null=False,db_column="Employee_id",to_field="username")
    # Name=models.CharField(max_length=50,null=False,verbose_name="full_name")
    # Team= models.CharField(verbose_name="team",max_length=20)
    # Role= models.CharField(verbose_name="role",max_length=20)
    # Designation=models.CharField(max_length=50,null=True,verbose_name="designation")
    # Email_id=models.CharField(max_length=50,verbose_name="email_id")
    # Photo_link=models.ImageField(verbose_name="image_link",upload_to="profile_images/",blank=True,null=True,default=None)

# class infra_emp_details(models.Model):
    # class Meta:
    #     db_table='team_infra"."infra_employee_details'
    #     verbose_name = "Infra Employee "
    #     verbose_name_plural = "Infra Employees"
    
    # Employee=models.OneToOneField(User, verbose_name="employee_id", on_delete=models.CASCADE,primary_key=True,null=False,db_column="Employee_id",to_field="username")
    # Name=models.CharField(max_length=50,null=False,verbose_name="full_name")
    # Team= models.CharField(verbose_name="team",max_length=20)
    # Role= models.CharField(verbose_name="role",max_length=20)
    # Designation=models.CharField(max_length=50,null=True,verbose_name="designation")
    # Email_id=models.CharField(max_length=50,verbose_name="email_id")
    # Photo_link=models.ImageField(verbose_name="image_link",upload_to="profile_images/",blank=True,null=True,default=None)
    
# class team_manage(models.Model):
    # class Meta:
    #     db_table='team_management"."management_team'
    #     verbose_name = "Management Team"
    #     verbose_name_plural = "Management Teams"
        
    # Employee=models.OneToOneField(User, verbose_name="employee_id", on_delete=models.CASCADE,primary_key=True,null=False,db_column="Employee_id",to_field="username")
    # Name=models.CharField(max_length=50,null=False,verbose_name="full_name")
    # Role= models.CharField(verbose_name="role",max_length=20)
    # Email_id=models.CharField(max_length=50,verbose_name="email_id")
    # Photo_link=models.ImageField(verbose_name="image_link",upload_to="profile_images/",blank=True,null=True,default=None)

# A model for "Roles" table
class Roles(models.Model):
    role_id=models.AutoField(primary_key=True,auto_created=True)
    role_name=models.CharField(max_length=20,unique=True,null=True)
    total_count=models.IntegerField(default=0,null=False,verbose_name="count")
    class Meta:
        db_table='team_management"."roles'
        verbose_name="role"
        verbose_name_plural="roles"
        
# A model for "Branches" table
class Branch(models.Model):
    branch_id=models.SmallAutoField(primary_key=True,auto_created=True,verbose_name="id",editable=False)
    branch_name=models.CharField(max_length=25,unique=True,null=True,verbose_name="branch")
    class Meta:
        db_table='team_management"."Branches'
        verbose_name="branch"
        verbose_name_plural="branches"
        
# # A model for "Designations" table
class Designation(models.Model):
    class Meta:
        db_table='team_management"."designations'
        verbose_name="designation"
        verbose_name_plural="designations"
    designation=models.CharField(max_length=50,unique=True,null=True)
    total_count=models.IntegerField(default=0,null=False,verbose_name="count")

# A model for "Profiles" table
class Profile(models.Model):

    Employee_id= models.OneToOneField(User,verbose_name="employee_id", on_delete=models.CASCADE,primary_key=True,db_column="Employee_id",to_field="username",related_name="accounts_profile",db_index=True)
    Role= models.ForeignKey(Roles,verbose_name="role",on_delete=models.CASCADE,db_column="Role",related_name="Employee_roles",null=True)
    Designation=models.ForeignKey("Designation",verbose_name="designation",db_column="Designation",on_delete=models.CASCADE,related_name="designations",null=True)
    Branch= models.ForeignKey("Branch",verbose_name="branch",on_delete=models.CASCADE,db_column="Branch",related_name="branches",null=True)
    Name=models.CharField(verbose_name="full_name",max_length=50,null=True)
    Email_id=models.EmailField(verbose_name="email_id",max_length=254,unique=True,validators=[validate_email])
    Date_of_birth=models.DateField(verbose_name="date_of_birth",auto_now=False, auto_now_add=False,null=True)
    Photo_link=models.ImageField(verbose_name="image_link", upload_to="profile_images/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    Date_of_join=models.DateField(verbose_name="date_of_joining",auto_now=False, auto_now_add=False,null=True)
    
    class Meta:
        verbose_name = "Employee Profile"
        verbose_name_plural = "Employees Profile"
        ordering=["-Name"]
        indexes = [
        models.Index(fields=['Role',"Designation"]),
    ]
        
    def __str__(self):
        return f"{self.Employee_id.username} - {self.Role}"
    
# A model for "Management_Profiles" table
class management_Profile(models.Model):
    Employee=models.OneToOneField(User,on_delete=models.PROTECT,to_field="username",null=False,related_name="management")
    Role= models.ForeignKey(Roles,verbose_name="role",on_delete=models.CASCADE,db_column="Role",related_name="management_roles",null=True)
    Name=models.CharField(verbose_name="full_name",max_length=50,null=True)
    Email_id=models.EmailField(verbose_name="email_id",max_length=254,unique=True,validators=[validate_email])
    Date_of_birth=models.DateField(verbose_name="date_of_birth",auto_now=False, auto_now_add=False,null=True)
    Photo_link=models.ImageField(verbose_name="image_link", upload_to="profile_images/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    Date_of_join=models.DateField(verbose_name="date_of_joining",auto_now=False, auto_now_add=False,null=True)

    class Meta:
        db_table='team_management"."management_profiles'
        verbose_name="management_profile"
        ordering=["-Date_of_join","Role"]
    def __str__(self):
        return f"{self.Role.role_name}-{self.Name}"
    
# Roles.objects.filter(role_name="Admin").update(role_name="ADMIN")        
# Roles.objects.filter(role_name="MD").update(role_name="MD")        
# Roles.objects.filter(role_name="Employee").update(role_name="EMPLOYEE")        
# Roles.objects.filter(role_name="Intern").update(role_name="INTERN")        
# Roles.objects.filter(role_name="TeamLead").update(role_name="TEAMLEAD")        

# Branch.objects.create(branch_name="Farm Core")
# Branch.objects.create(branch_name="Farm Tech")
# Branch.objects.create(branch_name="Infra Core")
# Branch.objects.create(branch_name="Infra Tech")
# Branch.objects.create(branch_name="Technology")







