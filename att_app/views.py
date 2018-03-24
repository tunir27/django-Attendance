from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from att_app.forms import RegistrationForm,FilterAttendance,VerifyForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student_Details,Student_Attendance,Token
from .serializers import StudentDetailsSerializer,TokenSerializer,StudentAttendanceSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from time import gmtime, strftime
import requests
from django.utils.html import escape
from datetime import date
from io import BytesIO
from .pdf_utils import PdfPrint

import itertools
import functools



@login_required(login_url='/login/')
def successful_login(request):
    ntime=strftime("%H", gmtime())
##    if int(ntime) > 8:
##        d=Student_Attendance.objects.all()
##        f=Student_Details.objects.filter(~Q(st_id__in=d.values_list('st_id',flat=True)))
##        for data in f:
##            ntime=strftime("%d/%m/%y", gmtime())
##            r=requests.post('http://127.0.0.1:8000/dashboard/apia/',data={'st_id':data.st_id,'date':ntime,'status':'0'})
    #http_date=''
    print(request.POST)


    form = VerifyForm(request.POST or None)
    http_data=request.POST.get('data')
    print(http_data)
    if http_data:
        http_status,http_sid,http_vdate = http_data.split(",")
    else:
        http_sid=None
        http_status=None
        http_vdate = None
##    http_sid=request.POST.get('id')
##    http_status=request.POST.get('status')
##    http_vdate = request.POST.get('date')
    print(http_sid)
    print(http_status)
    print(http_vdate)
    if http_sid and http_status and http_vdate:
        r=requests.post('http://127.0.0.1:8000/dashboard/apia/',data={'st_id':http_sid,'date':http_vdate,'status':http_status})
        print(r.content)



    form = FilterAttendance(request.POST or None)
    http_uid=request.session['username']
    user = get_user_model()
    uid=user.objects.get(sid=http_uid)
    staff_value=uid.is_staff
    print(staff_value)
    http_date = request.POST.get('date_id')
    http_class = request.POST.get('class_id')
    http_sec = request.POST.get('sec_id')

    if staff_value:
        date_item=Student_Attendance.objects.values('date').distinct()
        class_item=Student_Details.objects.values('s_class').distinct()
        section_item=Student_Details.objects.values('sec').distinct()
    else:
        date_item=Student_Attendance.objects.values('date').distinct()
        class_item=Student_Details.objects.filter(st_id=user.objects.get(sid=http_uid)).values('s_class')
        section_item=Student_Details.objects.filter(st_id=user.objects.get(sid=http_uid)).values('sec')


    if http_date and http_class and http_sec and staff_value:
        stu_count=Student_Details.objects.filter(s_class=http_class,sec=http_sec).count()
        stu_det=Student_Details.objects.filter(s_class=http_class,sec=http_sec)
        stu_att=Student_Attendance.objects.filter(date=http_date,st_id__in=stu_det.values_list('st_id',flat=True))
        att_count=Student_Attendance.objects.filter(date=http_date,st_id__in=stu_det.values_list('st_id',flat=True)).count()
    elif http_date and http_class and http_sec and not staff_value:
        stu_count=Student_Details.objects.filter(s_class=http_class,sec=http_sec).count()
        stu_det=Student_Details.objects.filter(st_id=uid,s_class=http_class,sec=http_sec)
        stu_att=Student_Attendance.objects.filter(date=http_date,st_id__in=stu_det.values_list('st_id',flat=True))
        att_count=Student_Attendance.objects.filter(date=http_date,st_id__in=stu_det.values_list('st_id',flat=True)).count()
    else:
        stu_count=0
        stu_att=''
        stu_det=''
        att_count=0

    return render(request,'dashboard.html',{"counter": functools.partial(next, itertools.count()),'stu_count':stu_count,'stu_att':stu_att,'stu_det':stu_det,'date_item':date_item,'class_item':class_item,'section_item':section_item,'att_count':att_count,'staff_value':staff_value,})

def pdf_test(request):
    attendance = Student_Attendance.objects.all()
    details = Student_Details.objects.all()
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
    response['Content-Disposition'] =\
        'attachement; filename={0}.pdf'.format(filename)
    buffer = BytesIO()
    report = PdfPrint(buffer, 'A4')
    pdf = report.report(attendance,details, 'Student Attendance data')
    response.write(pdf)
    return response



class ApiDetails(APIView):
    def get(self, request,std_id,format=None):
        try:
            http_stdid = Student_Details.objects.filter(st_id=std_id)
        except Student_Details.DoesNotExist:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
        serializer = StudentDetailsSerializer(http_stdid)
        return Response(serializer.data)
    def post(self, request, format=None):
        pstd_id = request.POST.get('st_id')
        User = get_user_model()
        if User.objects.filter(sid=pstd_id).exists():
            serializer = StudentDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
class ApiAttendance(APIView):
    def get(self, request,std_id,format=None):
        try:
            http_stdid = Student_Attendance.objects.filter(st_id=std_id)
        except Student_Attendance.DoesNotExist:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
        serializer = StudentAttendanceSerializer(http_stdid,many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        pstd_id = request.POST.get('st_id')
        p_date = request.POST.get('date')
        User = get_user_model()
        if User.objects.filter(sid=pstd_id).exists():
            uid=User.objects.filter(sid=pstd_id)
            http_date = Student_Attendance.objects.get(st_id=uid[0],date=p_date)
            print(http_date)
            serializer = StudentAttendanceSerializer(http_date,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
class ApiLogin(APIView):
    def get(self, request,format=None):
        u_id = request.GET.get('uid')
        password = request.GET.get('password')
        user = authenticate(sid=u_id, password=password)
        if user is None:
            return Response("Login error",status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Login successfull",status=status.HTTP_201_CREATED)
    def post(self, request, format=None):
        u_id = request.POST.get('uid')
        password = request.POST.get('password')
        token = request.POST.get('token')
        try:
            http_token = Token.objects.get(uid=u_id)
        except Token.DoesNotExist:
            http_token=''
        user = authenticate(sid=u_id, password=password)
        if user is None:
            return Response("Login error",status=status.HTTP_404_NOT_FOUND)
        else:
            if token:
                if http_token:
                    serializer = TokenSerializer(http_token,data=request.data)
                else:
                    serializer = TokenSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response("Login successfull token not supplied",status=status.HTTP_201_CREATED)

