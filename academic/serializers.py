from rest_framework import serializers

from academic.models import course, question_pattern, student, subject
from settings.models import co_import

class course_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = '__all__'

class subject_serializer(serializers.ModelSerializer):
    course_details = course_serializer()
    class Meta:
        model = subject
        fields = "__all__"

class course_detail_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['degree','course_name','department']

class student_serializer(serializers.ModelSerializer):
    course_details = course_detail_serializer()
    class Meta:
        model = student
        fields = "__all__"

class degree_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['degree']

class coursename_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['course_name']

class department_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['department','course_name']


class depart_serializer(serializers.ModelSerializer):
    class Meta:
        model = course
        fields = ['department']

class co_import_serializer(serializers.ModelSerializer):
    class Meta:
        model = co_import
        fields = ['co_number']

class question_serializer(serializers.ModelSerializer):
    department = depart_serializer()
    co_number = co_import_serializer()
    class Meta:
        model = question_pattern
        fields = "__all__"


# class YourModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = question_pattern
#         fields = '__all__'  

 