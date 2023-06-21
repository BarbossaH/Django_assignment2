import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


#model - 1 Semester

class Semester(models.Model):
      semester_choices = (   
        (1, "Spring"),
        (2, "Fall"), ) 
      id = models.AutoField(primary_key=True)
      year = models.IntegerField(default=datetime.datetime.now().year)
      semester = models.IntegerField(default=1, choices= semester_choices)

      def __str__(self):
        return f"{self.year}-{'Spring' if self.semester == 1 else 'Fall'}"
    
#model - 2 Course

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    semesters = models.ManyToManyField(Semester,  blank=True)

    def __str__(self):
        return f"{self.name} - {self.id}"

#model - 3 Class
class Class(models.Model):
    number = models.IntegerField(default=1)
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
      return f"{self.number}-{self.id}-{self.semester}-{self.course}-{self.lecturer}"
    

#model - 4 Lecturer
class Lecturer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='lecturer_profile')
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, null=True)
    DOB = models.DateField(default=None)

    def __str__(self):
      return f"Lecturer:{self.user.first_name}  {self.user.last_name}"

#model - 5 Student
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_profile')
    # email = models.EmailField(max_length=100)
    DOB = models.DateField(default=None)
    def __str__(self):
        return f"{self.id}-{self.user.first_name} {self.user.last_name}"
    

#model - 6 StudentEnrollment

class StudentEnrollment(models.Model):
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrolled_student = models.ForeignKey(Student,on_delete=models.CASCADE)
    enrollTime = models.DateField(auto_now_add=True)
    gradeTime = models.DateField(null=True, blank=True)
    #grade
    mark = models.CharField(max_length=8)

    def __str__(self):
      return self.mark
    
