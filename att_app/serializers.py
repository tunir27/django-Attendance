from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student_Details,Token,Student_Attendance,Teacher_Details

class StudentDetailsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Student_Details
        fields = ('st_id','first_name','last_name','dob','address','g_name','phone','s_class','sec')

class TeacherDetailsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Teacher_Details
        fields ='__all__'


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
        staff_value = serializers.SerializerMethodField()
        fields=('uid','token')

        def get_staff_value(self, obj):
            print(self.context['request'].user)
            user=get_user_model()
            staff_value=user.objects.filter(sid=obj.uid)
            return (staff_value)
