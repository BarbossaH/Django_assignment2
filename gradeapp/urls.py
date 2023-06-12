from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gradeapp import views
from gradeapp.viewsets import  UserViewSet

# from blog.viewsets import PostList, PostDetail
from gradeapp import viewsets
router = DefaultRouter()
router.register("users", UserViewSet)
router.register("students", viewsets.StudentViewSet)
router.register("lecturers", viewsets.LecturerViewSet)
router.register("semester", viewsets.SemesterViewSet)

urlpatterns = [  
    path('addstudent/',views.createStudent),
    path('addlecturer/',views.createLecturer),
    path('addsemester/',views.createSemester),
    path("", include(router.urls))
]