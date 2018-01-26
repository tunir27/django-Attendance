from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('att', views.view_data, name='Attendance'),
    path('api/<str:std_id>/', views.get_data, name='Student Attendance Api'),
    path('api/save/', views.save_data, name='Student Attendance Api Save'),
    path('apid/<str:stu_id>/', views.get_stddata, name='Student Details Api'),
]

