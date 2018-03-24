from rest_framework import serializers
from .models import Student_Details,Token,Student_Attendance

class StudentDetailsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Student_Details
        fields = ('st_id','first_name','last_name','dob','address','g_name','phone')

class StudentAttendanceSerializer(serializers.ModelSerializer):
    """Meta class to map serializer's fields with the model fields."""
    class Meta:
        model = Student_Attendance
        fields=('st_id','date','in_time','out_time','duration','status')



class TokenSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model=Token
        fields=('uid','token')
