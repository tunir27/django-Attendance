from django.db import models
# Create your models here.
class Student_Details(models.Model):
    name = models.CharField(max_length=50, help_text="Enter the Student Name",verbose_name="Student Name")
    stu_id = models.CharField(max_length=15, help_text="Enter the Student ID",verbose_name="Student ID",primary_key=True)
    address=models.CharField(max_length=50, help_text="Enter the Student Address",verbose_name="Student Address",null=True)
    g_name=models.CharField(max_length=50, help_text="Enter the Student Guardian Name",verbose_name="Guardian Name",null=True)
    phone=models.CharField(max_length=15, help_text="Enter Guardian Number",verbose_name="Guardian Phone",null=True)
    def __str__(self):
        return self.name
class Student_Attendance(models.Model):
    std_id=models.ForeignKey('Student_Details', on_delete=models.SET_NULL, null=True)
    date=models.CharField(max_length=15, help_text="Enter the Date",verbose_name="Date",default='00/00/00')
    in_time= models.CharField(max_length=15, help_text="Enter the IN Time",verbose_name="IN Time",default='00:00:00')
    out_time=models.CharField(max_length=15, help_text="Enter the OUT Time",verbose_name="OUT Time",null=True,blank=True)
    duration=models.CharField(max_length=15, help_text="Enter the Duration",verbose_name="Duration",null=True,blank=True)
    status = models.CharField(max_length=1, help_text="Enter the Status",verbose_name="Student Status",default='0')
    def __str__(self):
        return str(self.std_id) 
