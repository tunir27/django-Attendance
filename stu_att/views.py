from django.shortcuts import render
from .models import Student_Details,Student_Attendance
from rest_framework.response import Response
from rest_framework import status
from .serializers import AttendanceSerializer,StudentDetailsSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

# Create your views here.
def view_data(request):
    data = Student_Attendance.objects.all()
    return render(request, 'Attendance.html', {'data': data})


class ApiDetails(APIView):
    def get(self, request,stu_id, format=None):
        try:
            http_stdid = Student_Details.objects.get(stu_id=stu_id)
        except Student_Details.DoesNotExist:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
        serializer = StudentDetailsSerializer(http_stdid)
        return Response(serializer.data)


class ApiAttendance(APIView):
    def get(self, request,std_id, format=None):
        try:
            http_stdid = Student_Attendance.objects.get(std_id=std_id)
        except Student_Attendance.DoesNotExist:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(http_stdid)
        return Response(serializer.data) 
    def post(self, request, format=None):
        pstd_id = request.POST.get('std_id')
        try:
            http_stdid = Student_Attendance.objects.get(std_id=pstd_id)
        except Student_Attendance.DoesNotExist:
            return Response("Student ID error",status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(http_stdid,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
