from django.contrib.auth.models import User
from gradeapp.models import Student, Lecturer,Semester,Course,Class,StudentEnrollment
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'token']
        # fields = "__all__"

        extra_kwargs = {'password':{
            'write_only': True,
            'required': True
        }}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user
   
    def get_token(self, obj):
        try:
            token = Token.objects.get(user=obj)
            print(token.__dict__["key"])
            return token.__dict__["key"]
        except Token.DoesNotExist:
            return None
        
class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source = 'user.email',read_only=True)
    username = serializers.CharField(source = 'user.username',read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'username','first_name','last_name',  'email', 'DOB']

class LecturerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source = 'user.email',read_only=True)
    username = serializers.CharField(source = 'user.username',read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Lecturer
        fields = ['id','username','first_name','last_name', 'course', 'email', 'DOB']

class SemesterSerializer(serializers.ModelSerializer):

    def get_semester(self, obj):
        return "Spring" if obj.semester == 1 else "Fall"
    class Meta:
        model = Semester
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"    

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"
class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = "__all__"