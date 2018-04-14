from django.db import models
import login
from django.conf import settings
# Create your models here.
class Student_Details(models.Model):
    st_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,limit_choices_to={'is_staff': False})
    first_name=models.CharField(max_length=50, help_text="Enter the First-Name",verbose_name="First Name",null=True)
    last_name=models.CharField(max_length=50, help_text="Enter the Last Name",verbose_name="Last Name",null=True)
    dob=models.DateField(max_length=8,help_text="Enter Date of Birth",verbose_name="Date of Birth",null=True)
    address=models.CharField(max_length=50, help_text="Enter the Address",verbose_name="Address",null=True)
    g_name=models.CharField(max_length=50, help_text="Enter the Student Guardian Name",verbose_name="Guardian Name",null=True)
    phone=models.CharField(max_length=15, help_text="Enter Guardian Number",verbose_name="Guardian Phone",null=True)
    s_class=models.CharField(max_length=1, help_text="Enter Student Class",verbose_name="Student Class",null=True)
    sec=models.CharField(max_length=1, help_text="Enter Student Section",verbose_name="Student Section",null=True)
    email = models.EmailField(max_length=70,help_text="Enter Email",verbose_name="Email",blank=True,null=True,unique=True)
    def __str__(self):
        return str(self.st_id)
class Teacher_Details(models.Model):
    t_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,limit_choices_to={'is_staff': True})
    first_name=models.CharField(max_length=50, help_text="Enter the First-Name",verbose_name="First Name",null=True)
    last_name=models.CharField(max_length=50, help_text="Enter the Last Name",verbose_name="Last Name",null=True)
    dob=models.DateField(max_length=8,help_text="Enter Date of Birth",verbose_name="Date of Birth",null=True)
    address=models.CharField(max_length=50, help_text="Enter the Address",verbose_name="Address",null=True)
    phone=models.CharField(max_length=15, help_text="Enter Phone Number",verbose_name="Phone No",null=True)
    def __str__(self):
        return str(self.t_id)
class Student_Attendance(models.Model):
    st_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,limit_choices_to={'is_staff': False})
    date=models.CharField(max_length=15, help_text="Enter the Date",verbose_name="Date",null=True)
    in_time= models.CharField(max_length=15, help_text="Enter the IN Time",verbose_name="IN Time",null=True)
    out_time=models.CharField(max_length=15, help_text="Enter the OUT Time",verbose_name="OUT Time",null=True,blank=True)
    duration=models.CharField(max_length=15, help_text="Enter the Duration",verbose_name="Duration",null=True,blank=True)
    status = models.CharField(max_length=1, help_text="Enter the Status",verbose_name="Student Status",null=True)
    def __str__(self):
        return (str(self.st_id)+' '+str(self.date)) 
class Token(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    token= models.CharField(max_length=300,help_text="Enter the token",verbose_name="Token",null=True)
    def __str__(self):
        return str(self.uid)
