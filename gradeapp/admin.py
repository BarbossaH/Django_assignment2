from django.contrib import admin

from .models import   Semester,Class, Student,StudentEnrollment, Lecturer, Course
# Register your models here.
admin.site.register(Semester)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(StudentEnrollment)
admin.site.register(Lecturer)
admin.site.register(Course)