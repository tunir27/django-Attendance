from django.contrib import admin
from .models import Student_Details,Teacher_Details,Student_Attendance,Token
# Register your models here.
admin.site.register(Student_Details)
admin.site.register(Teacher_Details)
admin.site.register(Student_Attendance)
admin.site.register(Token)
