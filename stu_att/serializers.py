from rest_framework import serializers
from .models import Student_Attendance,Student_Details

class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Student_Attendance
        fields = ('std_id', 'date', 'in_time', 'out_time','duration','status')
class StudentDetailsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Student_Details
        fields = ('name', 'stu_id', 'address','g_name','phone')
