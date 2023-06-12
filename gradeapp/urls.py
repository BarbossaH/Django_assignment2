from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gradeapp import views
from gradeapp.viewsets import  UserViewSet

# from blog.viewsets import PostList, PostDetail
from gradeapp.viewsets import StudentViewSet
router = DefaultRouter()
router.register("users", UserViewSet)
router.register("students", StudentViewSet)

urlpatterns = [  
    path('addstudent/',views.createStudent),
    path("", include(router.urls))
]