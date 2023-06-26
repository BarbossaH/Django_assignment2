from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gradeapp import views
from gradeapp.viewsets import  UserViewSet

# from blog.viewsets import PostList, PostDetail
from gradeapp import viewsets
router = DefaultRouter()
router.register("users", viewsets.UserViewSet)
router.register("students", viewsets.StudentViewSet)
router.register("lecturers", viewsets.LecturerViewSet)
router.register("semester", viewsets.SemesterViewSet)
router.register("course", viewsets.CourseViewSet)
router.register("class", viewsets.ClassViewSet)
router.register("studentenrollment", viewsets.StudentEnrollmentViewSet)

urlpatterns = [  
    path('addstudent/',views.createStudent),
    path('students/<int:id>/edit/',views.updateStudent),
    path('addlecturer/',views.createLecturer),
    path('lecturers/<int:id>/edit/',views.updateLecturer),
    path('addsemester/',views.createSemester),
    path('semester/<int:id>/edit/',views.updateSemester),
    path('addcourse/',views.createCourse),
    path('course/<int:id>/edit/',views.updateCourse),
    path('addclass/',views.createClass),
    path('classes/<int:id>/edit/',views.updateClass),
    path('addstudentenrollment/',views.createStudentEnrollment),
    path('studentenrollment/<int:id>/edit/',views.updateStudentEnrollment),
    path('upload/',views.uploadExcel),
    path('sendemail/<int:id>/',views.send_email),
    path("", include(router.urls))
]