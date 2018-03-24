from django.urls import path
from . import views
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('att/',views.successful_login,name='Attendance'),
    path('att/student_details',TemplateView.as_view(template_name="students_details.html"),name='Student Details'),
    path('apid/', views.ApiDetails.as_view(), name='Student Details Api Save'),
    path('apid/<str:std_id>/', views.ApiDetails.as_view(), name='Student Details Api'),
    path('apia/', views.ApiAttendance.as_view(), name='Student Attendance Api Save'),
    path('apia/<str:std_id>/', views.ApiAttendance.as_view(), name='Student Attendance Api'),
    path('lapi/', views.ApiLogin.as_view(), name='Login Api'),
    path('pdf/',views.pdf_test,name='Pdf'),
]
