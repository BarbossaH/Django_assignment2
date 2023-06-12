from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

# from gradeapp.models import Post
from gradeapp.serializers import StudentSerializer
from gradeapp.models import Student

@api_view(['GET'])
def index(request):
    # if request.user.is_authenticated:
    print(1232321321)
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return HttpResponse(serializer.data)
    # return HttpResponse("Hello n11obody")

@api_view(['GET'])
def getStudentDetail(request, id):
    student = Student.objects.get(id=id)
    serializer = StudentSerializer(student, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createStudent(request):
    # data = JSONParser().parse(request)
    user_data = request.data.pop('user')
    print(user_data)
    user = User.objects.create(**user_data)
    token = Token.objects.create(user=user)
    student_group = Group.objects.get(name='Student') 
    print(student_group)
    user.groups.add(student_group)
    student = Student.objects.create(user=user, **request.data)
    serializer = StudentSerializer(student, many=False)
    return Response(serializer.data)
    # serializer = StudentSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data)
    # return Response(serializer.errors)

@api_view(['PUT'])
def updateStudent(request, id):
    student = Student.objects.get(id=id)
    serializer = StudentSerializer(instance=student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def deleteStudent(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return Response("Deleted")
