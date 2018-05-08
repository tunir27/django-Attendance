from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from .forms import RegistrationForm, FilterAttendance, VerifyForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student_Details, Student_Attendance, Token,Teacher_Details
from .serializers import StudentDetailsSerializer, TokenSerializer, StudentAttendanceSerializer,TeacherDetailsSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
import datetime
import requests
from django.utils.html import escape
from datetime import date
from io import BytesIO
from .pdf_utils import PdfPrint
from django.db.models import Q
import itertools
import functools
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from Project.settings import DEFAULT_FROM_EMAIL,FCM_SERVER_API
from django.views.generic import *
from .forms import PasswordResetRequestForm,SetPasswordForm,ContactUsForm


from pyfcm import FCMNotification


@login_required(login_url='/login/')
def successful_login(request):
    now = datetime.datetime.now()
    day=now.weekday()
    ntime = now.strftime("%H")
    ndate=now.strftime("%d/%m/%y")
    if not day==6:
        if int(ntime) >= 7:
            d=Student_Attendance.objects.filter(date=ndate)
            f=Student_Details.objects.filter(~Q(st_id__in=d.values_list('st_id',flat=True))).order_by('st_id')
            for data in f:
                r=requests.post('https://attendanceproject.herokuapp.com/home/apia/',data={'st_id':data.st_id,'date':ndate,'status':'0'})
                #r=requests.post('http://127.0.0.1:8000/home/apia/',data={'st_id':data.st_id,'date':ndate,'status':'0'})
                print(r.content)
        if int(ntime)>= 15:
            d=Student_Attendance.objects.filter(date=ndate,status="1").order_by('st_id')
            for data in d:
                if not data.out_time:
                    r=requests.post('https://attendanceproject.herokuapp.com/home/apia/',data={'st_id':data.st_id,'date':ndate,'status':'0','out_time':'--'})
                    #r=requests.post('http://127.0.0.1:8000/home/apia/',data={'st_id':data.st_id,'date':ndate,'status':'0'})
                    print(r.content)
                if not data.in_time:
                    r=requests.post('https://attendanceproject.herokuapp.com/home/apia/',data={'st_id':data.st_id,'date':ndate,'status':'0','in_time':'--'})
                    #r=requests.post('http://127.0.0.1:8000/home/apia/',data={'st_id':data.st_id,'date':ndate,'status':'0'})
                    print(r.content)
                
    form = VerifyForm(request.POST or None)
    http_data = request.POST.get('data')
    print(http_data)
    if http_data:
        http_status, http_sid, http_vdate = http_data.split(",")
    else:
        http_sid = None
        http_status = None
        http_vdate = None
    if http_sid and http_status and http_vdate:
        now = datetime.datetime.now()
        ntime=now.strftime("%H:%M:%S")
        if http_status=="1":
            r = requests.post('https://attendanceproject.herokuapp.com/home/apia/',
                              data={'st_id': http_sid, 'date': http_vdate,'in_time':ntime, 'status': http_status,'notif_s':"2"})
##            r = requests.post('http://127.0.0.1:8000/home/apia/',
##                              data={'st_id': http_sid, 'date': http_vdate,'in_time':ntime, 'status': http_status,'notif_s':"2"})
        if http_status=="0":
            r = requests.post('https://attendanceproject.herokuapp.com/home/apia/',data={'st_id': http_sid, 'date': http_vdate,'in_time':"", 'status': http_status,'notif_s':"2"})
            #r = requests.post('http://127.0.0.1:8000/home/apia/',data={'st_id': http_sid, 'date': http_vdate,'in_time':"", 'status': http_status,'notif_s':"2"})
        print(r.content)

    form = FilterAttendance(request.POST or None)
    http_uid = request.session['username']
    user = get_user_model()
    uid = user.objects.get(sid=http_uid)
    staff_value = uid.is_staff
    request.session['staff_value']=staff_value
    http_date = request.POST.get('date_id')
    http_class = request.POST.get('class_id')
    http_sec = request.POST.get('sec_id')

    if staff_value:
        date_item = Student_Attendance.objects.values('date').distinct()
        class_item = Student_Details.objects.values('s_class').distinct()
        section_item = Student_Details.objects.values('sec').distinct()
    else:
        date_item = Student_Attendance.objects.values('date').distinct()
        class_item = Student_Details.objects.filter(st_id=user.objects.get(sid=http_uid)).values('s_class')
        section_item = Student_Details.objects.filter(st_id=user.objects.get(sid=http_uid)).values('sec')
        

    if http_date and http_class and http_sec:
        stu_det = Student_Details.objects.filter(s_class=http_class, sec=http_sec).order_by('st_id')
        stu_att = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det.values_list('st_id', flat=True)).order_by('st_id')
        att_count_a = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det.values_list('st_id', flat=True),status="0").count()
        att_count_p = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det.values_list('st_id', flat=True),status="1").count()



    if http_date and http_class and http_sec and staff_value:
        stu_count = Student_Details.objects.filter(s_class=http_class, sec=http_sec).count()
        stu_det = Student_Details.objects.filter(s_class=http_class, sec=http_sec).order_by('st_id')
        stu_att = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det.values_list('st_id', flat=True)).order_by('st_id')
    elif http_date and not http_class and not http_sec and not staff_value:
        stu_det=Student_Details.objects.filter(st_id=uid.sid).order_by('st_id')
        stu_det_all=Student_Details.objects.filter(s_class=stu_det[0].s_class, sec=stu_det[0].sec).order_by('st_id')
        stu_count = Student_Details.objects.filter(s_class=stu_det[0].s_class, sec=stu_det[0].sec).count()
        stu_att = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det.values_list('st_id', flat=True)).order_by('st_id')
        att_count_a = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det_all.values_list('st_id', flat=True),status="0").count()
        att_count_p = Student_Attendance.objects.filter(date=http_date, st_id__in=stu_det_all.values_list('st_id', flat=True),status="1").count()


    else:
        stu_count = 0
        stu_att = ''
        stu_det = ''
        att_count_a = 0
        att_count_p = 0


    
        



    return render(request, 'dashboard.html',
                  {"counter": functools.partial(next, itertools.count()), 'stu_count': stu_count, 'stu_att': stu_att,
                   'stu_det': stu_det, 'date_item': date_item, 'class_item': class_item, 'section_item': section_item,
                   'att_count_a': att_count_a,'att_count_p':att_count_p, 'staff_value': staff_value,'combined':zip(stu_att,stu_det)})


def site_history(request):

    class_item = Student_Details.objects.values('s_class').distinct()
    section_item = Student_Details.objects.values('sec').distinct()
    staff_value=request.session['staff_value']
    return render(request,'history.html',{'class_item':class_item,'section_item':section_item,'staff_value':staff_value})

@csrf_exempt
def pdf_test(request):
    http_stid=""
    print(request.POST)
    http_date=request.POST.get('date')
    http_class = request.POST.get('class_id')
    http_sec = request.POST.get('sec_id')
    http_uid = request.POST.get('uid')
    print(http_class)
    print(http_sec)
    print(http_date)
    pdf_type=0
    if http_uid:
        http_stid=http_uid
        pdf_type=1
    if request.POST.get('stu_id'):
        http_stid=request.POST.get('stu_id')
        pdf_type=1
    else:
        try:
            request.session['username']
            if not http_stid:
                pdf_type=1
                http_stid=request.session['username']
        except:
            pass
    d,m,y=http_date.split("/")
    user = get_user_model()
    if http_stid:
        uid = user.objects.filter(sid=http_stid)
    if http_class and http_sec:
        pdf_type=0
        details = Student_Details.objects.filter(s_class=http_class, sec=http_sec)
        attendance = Student_Attendance.objects.filter(date__contains=('/'+m+'/'), st_id__in=details.values_list('st_id', flat=True))
        pie=0
        filename = 'pdf_attendance' +" "+ http_class + "-"+ http_sec + " " + m + "," + y
    else:
        attendance = Student_Attendance.objects.filter(st_id=uid[0],date__contains=('/'+m+'/'))
        details = Student_Details.objects.filter(st_id=uid[0])
        pie=1
        for i in details:
            filename = 'pdf_attendance ' +" "+ i.first_name +" "+ i.last_name +" " + m + "," + y
    print(attendance)
    print(details)
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    response['Content-Disposition'] = \
        'attachement; filename={0}.pdf'.format(filename)
    buffer = BytesIO()
    report = PdfPrint(buffer, 'A4')
    pdf = report.report(attendance, details,http_date,pie, 'Student Attendance data',pdf_type)
    response.write(pdf)
    return response


class ContactUsView(FormView):
        template_name = "contact_form/contact_form.html"    #code for template is given below the view's code
        success_url = '/home/contact/'
        form_class = ContactUsForm
        
        @method_decorator(csrf_exempt)
        def dispatch(self, request, *args, **kwargs):
            return super(ContactUsView, self).dispatch(request, *args, **kwargs)
        def post(self, request, *args, **kwargs):
            '''
            A normal post request which takes input from field "name" and "subject" (in ContactUsForm). 
            '''
            print(request.POST)
            http_name=request.POST.get('c_name')
            http_subject=request.POST.get('c_subject')
            http_sid=request.POST.get('uid')
            if http_name==None and http_subject==None:
                form = self.form_class(request.POST)
                if form.is_valid():
                    name= form.cleaned_data["name"]
                    subject=form.cleaned_data["subject"]
            else:
                name=""
                subject=""
            user = get_user_model()
            if http_sid:
                http_stid=http_sid
            else:
                http_stid = request.session['username']
            uid = user.objects.filter(sid=http_stid)
            stu_det=""
            t_det=""
            if uid[0].is_staff:
                t_det=Teacher_Details.objects.filter(t_id=uid[0].sid)
            else:
                stu_det=Student_Details.objects.filter(st_id=uid[0].sid)
            c = {
                'email': 'attendrteam@gmail.com',
                'name': name,
                'content':subject,
                'user': 'Not Specified' ,
                'u_mail':'Not Specified'
                }
            if stu_det:
                if stu_det[0].email:
                    if name and subject:
                        c = {
                            'email': 'attendrteam@gmail.com',
                            'name': name,
                            'content':subject,
                            'user':uid[0],
                            'u_mail':stu_det[0].email
                            }
                    else:
                        c = {
                            'email': 'attendrteam@gmail.com',
                            'name': http_name,
                            'content':http_subject,
                            'user':uid[0],
                            'u_mail':stu_det[0].email
                            }
            elif t_det:
                if t_det[0].email:
                    if name and subject:
                        c = {
                            'email': 'attendrteam@gmail.com',
                            'name': name,
                            'content':subject,
                            'user':uid[0],
                            'u_mail':t_det[0].email
                            }
                    else:
                        c = {
                            'email': 'attendrteam@gmail.com',
                            'name': http_name,
                            'content':http_subject,
                            'user':uid[0],
                            'u_mail':t_det[0].email
                            }
            subject_template_name='contact_form/contact_form_subject.txt' 
            # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
            email_template_name='contact_form/contact_form_email.html'    
            # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            if stu_det:
                send_mail(subject, email, stu_det[0].email , ['attendrteam@gmail.com'], fail_silently=False)
            elif t_det:
                send_mail(subject, email, t_det[0].email , ['attendrteam@gmail.com'], fail_silently=False)
            if http_name and http_subject:
                return JsonResponse({"msg":"An email has been sent to the administration. We will get back to you soon."}, status=status.HTTP_201_CREATED)
            else:    
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to the administration. We will get back to you soon.')
                return result
                result = self.form_invalid(form)
                messages.error(request, 'No email id associated with this user')
                return result




class ResetPasswordRequestView(FormView):
        template_name = "account/test_template.html"    
        success_url = '/login/'
        form_class = PasswordResetRequestForm

        @staticmethod
        def validate_email_address(email):
            '''
            This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
            '''
            try:
                validate_email(email)
                return True
            except ValidationError:
                return False

        def post(self, request, *args, **kwargs):
            '''
            A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm). 
            '''
            form = self.form_class(request.POST)
            if form.is_valid():
                data= form.cleaned_data["email_or_username"]
            if self.validate_email_address(data) is True:                 #uses the method written above
                '''
                If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
                '''
                User = get_user_model()
                stu_det=""
                t_det=""
                try:
                    stu_det=Student_Details.objects.filter(email=data)
                    if not stu_det.exists():
                        t_det=Teacher_Details.objects.filter(email=data)
                except Student_Details.DoesNotExist:
                    t_det=Teacher_Details.objects.filter(email=data)
                print("t_det",t_det)
                if stu_det:
                    associated_users=User.objects.filter(sid=stu_det[0])
                elif t_det:
                    associated_users=User.objects.filter(sid=t_det[0])
                else:
                    associated_users=None
                if associated_users:
                    if stu_det.exists():
                        c = {
                            'email': stu_det[0].email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Attendr',
                            'uid': urlsafe_base64_encode(force_bytes(associated_users[0].pk)).decode(),
                            'user': associated_users[0],
                            'token': default_token_generator.make_token(associated_users[0]),
                            'protocol': 'http',
                            }
                    elif t_det.exists():
                        c = {
                            'email': t_det[0].email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Attendr',
                            'uid': urlsafe_base64_encode(force_bytes(associated_users[0].pk)).decode(),
                            'user': associated_users[0],
                            'token': default_token_generator.make_token(associated_users[0]),
                            'protocol': 'http',
                            }                        
                    subject_template_name='registration/password_reset_subject.txt' 
                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                    email_template_name='registration/password_reset_email.html'    
                    # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    if stu_det:
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [stu_det[0].email], fail_silently=False)
                    elif t_det:
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [t_det[0].email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
            else:
                '''
                If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
                '''
                User = get_user_model()
                associated_users= User.objects.filter(sid=data)
                    
                if associated_users:
                    if not associated_users[0].is_staff:
                        stu_det=Student_Details.objects.filter(st_id=associated_users[0].sid)
                        t_det=''
                    else:
                        t_det=Teacher_Details.objects.filter(t_id=associated_users[0].sid)
                        stu_det=''
                    if stu_det:
                        if not stu_det[0].email:
                            result = self.form_invalid(form)
                            messages.error(request, 'This username does does not have an email id.Please contact administrator.')
                            return result
                        c = {
                            'email': stu_det[0].email,
                            'domain': request.META['HTTP_HOST'], #or your domain
                            'site_name': 'Attendr',
                            'uid': urlsafe_base64_encode(force_bytes(associated_users[0].sid)).decode(),
                            'user': associated_users[0],
                            'token': default_token_generator.make_token(associated_users[0]),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        email_template_name='registration/password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [stu_det[0].email], fail_silently=False)
                        result = self.form_valid(form)
                        messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                        return result
                    elif t_det:
                        if not t_det[0].email:
                            result = self.form_invalid(form)
                            messages.error(request, 'This username does does not have an email id.Please contact administrator.')
                            return result
                        c = {
                            'email': t_det[0].email,
                            'domain': request.META['HTTP_HOST'], #or your domain
                            'site_name': 'Attendr',
                            'uid': urlsafe_base64_encode(force_bytes(associated_users[0].sid)).decode(),
                            'user': associated_users[0],
                            'token': default_token_generator.make_token(associated_users[0]),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        email_template_name='registration/password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [t_det[0].email], fail_silently=False)
                        result = self.form_valid(form)
                        messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                        return result
                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result
            messages.error(request, 'Invalid Input')
            return self.form_invalid(form)



class PasswordResetConfirmView(FormView):
    template_name = "account/test_template.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(sid=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)







class ApiDetails(APIView):
    def get(self, request, std_id, format=None):
        User = get_user_model()
        user_value=User.objects.filter(sid=std_id)
        if not user_value:
            return JsonResponse({"msg":"Student/Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
                
        if user_value[0].is_staff:
                http_stdid = Teacher_Details.objects.filter(t_id=std_id)
                serializer = TeacherDetailsSerializer(http_stdid, many=True)
        else:
                http_stdid = Student_Details.objects.filter(st_id=std_id)
                serializer = StudentDetailsSerializer(http_stdid, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pstd_id = request.POST.get('st_id')
        pt_id= request.POST.get('t_id')
        User = get_user_model()
        if pstd_id:
            user_value=User.objects.filter(sid=pstd_id)
        if pt_id:
            user_value=User.objects.filter(sid=pt_id)
        if user_value.exists():
            if user_value[0].is_staff:
                temp_tdet=Teacher_Details.objects.get(t_id=user_value[0])
                serializer = TeacherDetailsSerializer(temp_tdet,data=request.data)
            else:
                temp_sdet=Student_Details.objects.get(st_id=user_value[0])
                serializer = StudentDetailsSerializer(temp_sdet,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"msg":"Student/Teacher not found"}, status=status.HTTP_404_NOT_FOUND)


class ApiTeachAttendance(APIView):
    def post(self, request,format=None):
        h_class=request.POST.get('h_class')
        h_sec=request.POST.get('h_sec')
        h_date=request.POST.get('h_date')
        if not h_date:
            stu_det = Student_Details.objects.filter(s_class=h_class, sec=h_sec)
            date = Student_Attendance.objects.filter(st_id__in=stu_det.values_list('st_id', flat=True)).values('date').distinct()
            return JsonResponse({"date":list(date)})
        else:
            try:
                stu_det = Student_Details.objects.filter(s_class=h_class, sec=h_sec)
                stu_att = Student_Attendance.objects.filter(date=h_date, st_id__in=stu_det.values_list('st_id', flat=True))
            except Student_Attendance.DoesNotExist:
                return JsonResponse({"msg":"Value error"}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentAttendanceSerializer(stu_att.order_by('st_id'), many=True)
            serializer_name=StudentDetailsSerializer(stu_det.order_by('st_id'), many=True)
            return JsonResponse({"data":serializer.data,"name":serializer_name.data})





class ApiAttendance(APIView):
    def get(self, request, std_id,format=None):
        try:
            http_stdid = Student_Attendance.objects.filter(st_id=std_id)
        except Student_Attendance.DoesNotExist:
            return JsonResponse({"msg":"Student ID error"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentAttendanceSerializer(http_stdid, many=True)
        return JsonResponse({"data":serializer.data})

    def post(self, request, format=None):
        pstd_id = request.POST.get('st_id')
        p_date = request.POST.get('date')
        http_status=request.POST.get('status')
        print(request.POST)
        if not http_status:
            try:
                http_stdid = Student_Attendance.objects.filter(st_id=pstd_id,date=p_date)
            except Student_Attendance.DoesNotExist:
                return Response("Student ID error", status=status.HTTP_404_NOT_FOUND)
            serializer = StudentAttendanceSerializer(http_stdid, many=True)
            return JsonResponse({"data":serializer.data})
        else:
            User = get_user_model()
            if User.objects.filter(sid=pstd_id).exists():
                uid = User.objects.filter(sid=pstd_id)
                try:
                    stu_a = Student_Attendance.objects.get(st_id=uid[0], date=p_date)
                    if stu_a.in_time and http_status=="1":
                        new_data=request.data.copy()
                        new_data['in_time']=stu_a.in_time
                    else:
                        new_data=""
                except Student_Attendance.DoesNotExist:
                    stu_a = None
                if stu_a:
                    print("new_data",new_data)
                    if new_data:
                        serializer = StudentAttendanceSerializer(stu_a.order_by('st_id'), data=new_data)
                    else:
                        serializer = StudentAttendanceSerializer(stu_a.order_by('st_id'), data=request.data)
                else:
                    serializer = StudentAttendanceSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    notif_s= request.POST.get('notif_s')
                    message_title = "Student Attendance"
                    registration_id=None
                    if notif_s == "1":
                        push_service = FCMNotification(api_key=FCM_SERVER_API)
                        try:
                            tokenq=Token.objects.get(uid=uid[0])
                            registration_id = tokenq.token
                        except:
                            registration_id=None
                        stu_det=Student_Details.objects.get(st_id=uid[0])
                        if stu_a.status=="1":
                            message_body = stu_det.first_name + " has entered the school at " + stu_a.in_time
                        elif stu_a.status=="0":
                            message_body = stu_det.first_name + " has left the school at " + stu_a.out_time
                    elif notif_s == "2":
                        push_service = FCMNotification(api_key=FCM_SERVER_API)
                        try:
                            tokenq=Token.objects.get(uid=uid[0])
                            registration_id = tokenq.token
                        except:
                            registration_id=None
                        stu_det=Student_Details.objects.get(st_id=uid[0])
                        now = datetime.datetime.now()
                        ntime = now.strftime("%H:%M:%S")
                        if stu_a.status=="1":
                            message_body = stu_det.first_name + " has been marked present at " + ntime + " by the authorities."
                        elif stu_a.status=="0":
                            message_body = stu_det.first_name + " has been marked absent at " + ntime + " by the authorities."
                    if registration_id:
                        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body,sound="Default")
                        print(result)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({"msg":"Student ID error"}, status=status.HTTP_404_NOT_FOUND)


class ApiLogin(APIView):

     def post(self, request, format=None):
        u_id = request.POST.get('uid')
        password = request.POST.get('password')
        token = request.POST.get('token')
        if not token:
            user = authenticate(sid=u_id, password=password)
            if user is None:
                return JsonResponse({"msg":"Login error"}, status=status.HTTP_404_NOT_FOUND)
            else:
                request.session['username']=user.sid
                return JsonResponse({"msg":"Login successfull"}, status=status.HTTP_201_CREATED)
        try:
            http_token = Token.objects.get(uid=u_id)
        except Token.DoesNotExist:
            http_token = ''
        user = authenticate(sid=u_id, password=password)
        if user is None:
            return JsonResponse({"msg":"Login error"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if token:
                if http_token:
                    serializer = TokenSerializer(http_token, data=request.data)
                else:
                    serializer = TokenSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    cus_data=serializer.data
                    cus_data['staff_value']=user.is_staff
                    return Response(cus_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

