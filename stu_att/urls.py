from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('att', views.view_data, name='Attendance'),
    path('api/<str:std_id>/', views.ApiAttendance.as_view(), name='Student Attendance Api'),
    path('api/', views.ApiAttendance.as_view(), name='Student Attendance Api Save'),
    path('apid/<str:stu_id>/', views.ApiDetails.as_view(), name='Student Details Api'),
]

