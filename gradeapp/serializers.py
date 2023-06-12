from django.contrib.auth.models import User
from gradeapp.models import Student, Lecturer,Semester
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
    class Meta:
        model = Student
        fields = ['id', 'first_name','last_name', 'studentId', 'email', 'DOB']

class LecturerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source = 'user.email',read_only=True)
    
    class Meta:
        model = Lecturer
        fields = ['id','first_name','last_name', 'staffId', 'email', 'DOB']

class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = "__all__"
    