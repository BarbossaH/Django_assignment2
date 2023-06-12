from django.contrib.auth.models import User
from gradeapp.models import Student
from rest_framework import viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

# from gradeapp.permissions import IsAuthorOrReadOnly
from gradeapp.serializers import  UserSerializer, StudentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer