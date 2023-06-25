from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from gradeapp.permissions import IsAuthorOrReadOnly,IsLecturer,IsStudent
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
# from gradeapp.models import Post
from gradeapp.serializers import StudentSerializer, LecturerSerializer,SemesterSerializer,CourseSerializer,ClassSerializer,StudentEnrollmentSerializer
from gradeapp.models import Student, Lecturer,Semester,Course,Class,StudentEnrollment



#create student
@api_view(['POST'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def createStudent(request):
    # print(request.data,99999999)
    data = request.data
    DOB = data.pop('DOB')
    username = data.get('username', None)
    if username and User.objects.filter(username=username).exists():
        error_message = "Username already exists."
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create(**data)
    print(user,"This is user")
    token = Token.objects.create(user=user)
    student_group = Group.objects.get(name='Student') 
    user.groups.add(student_group)
    student = Student.objects.create(user=user, DOB=DOB)
    serializer = StudentSerializer(data=request.data, many=False)
    if(serializer.is_valid()):
        # serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        user.delete()  # 如果保存失败，删除已创建的用户对象
        student.delete()  # 如果保存失败，删除已创建的学生对象
        return Response(serializer.errors)

#update student
@api_view(['PUT'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def updateStudent(request,id):
    # print(request.data, 1232321321)
    filtered_data = {key: value for key, value in request.data.items() if key != 'DOB'}
    print(filtered_data)
    serializer = StudentSerializer(data=filtered_data, many=False)
    if serializer.is_valid():
        # serializer.save()
        student = Student.objects.get(id=id)
        student.user.first_name = request.data['first_name']
        student.user.last_name = request.data['last_name']
        student.user.email = request.data['email']
        student.user.save()
        student.DOB = request.data['DOB']
        student.save()
        return Response(serializer.data)
    return Response(serializer.errors)
 



#create lecturer
@api_view(['POST'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def createLecturer(request):
    data = request.data
    DOB = data.pop('DOB')
    courseID = data.pop('course')
    is_exist = Course.objects.filter(id=courseID).exists()
    if not is_exist:
        error_message = "Course does not exist."
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    course = Course.objects.get(id=courseID)
    username = data.get('username', None)
    if username and User.objects.filter(username=username).exists():
        error_message = "Username already exists."
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create(**data)
    print(user,"This is user")
    token = Token.objects.create(user=user)
    lecturer_group = Group.objects.get(name='Lecturer') 
    # print(lecturer_group)
    user.groups.add(lecturer_group)
    serializer = LecturerSerializer(data=request.data, many=False)
    if serializer.is_valid():
        # serializer.save()
        lecturer = Lecturer.objects.create(user=user, course=course, DOB=DOB)

        return Response(serializer.data)
    return Response(serializer.errors)

#update lecturer 
@api_view(['PUT'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def updateLecturer(request,id):
    filtered_data = {key: value for key, value in request.data.items() if key != 'DOB'}
    print(filtered_data)
    serializer = LecturerSerializer(data=filtered_data, many=False)
    if serializer.is_valid():
        lecturer = Lecturer.objects.get(id=id)
        lecturer.user.first_name = request.data['first_name']
        lecturer.user.last_name = request.data['last_name']
        lecturer.user.email = request.data['email']
        lecturer.user.save()
        lecturer.DOB = request.data['DOB']
        lecturer.course = Course.objects.get(id=request.data['course'])
        lecturer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

#create semester
@api_view(['POST'])
@permission_classes([IsAdminUser])
def createSemester(request):
    serializer = SemesterSerializer(data=request.data, many=False)
    if serializer.is_valid():
        # serializer.save()
        semester = Semester.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

#update semester
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateSemester(request,id):
    serializer = SemesterSerializer(data=request.data, many=False)
    if serializer.is_valid():
        semester = Semester.objects.get(id=id)
        semester.year = request.data['year']
        semester.semester = request.data['semester']
        semester.save()
        return Response(serializer.data)
    return Response(serializer.errors)

#create course
@api_view(['POST'])
def createCourse(request):
    serializer = CourseSerializer(data=request.data, many=False)
    if serializer.is_valid():
        course = Course.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

#update course
@api_view(['PUT'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def updateCourse(request,id):
    serializer = CourseSerializer(data=request.data, many=False)
    if serializer.is_valid():
        course = Course.objects.get(id=id)
        course.name = request.data['name']
        course.code = request.data['code']
        course.semesters = Semester.objects.get(id=request.data['semesters'])
        course.save()
        return Response(serializer.data)
    return Response(serializer.errors)

#delete course
@api_view(['POST'])
def createClass(request):
    serializer = ClassSerializer(data=request.data, many=False)
    if serializer.is_valid():
        class_ = Class.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

#update class
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateClass(request,id):
    serializer= ClassSerializer(data=request.data, many=False)
    if serializer.is_valid():
        class_ = Class.objects.get(id=id)
        class_.semester = request.data['name']
        class_.number = request.data['number']
        class_.course = Course.objects.get(id=request.data['course'])
        class_.save()
        return Response(serializer.data)


#create enrollment
@api_view(['POST'])
def createStudentEnrollment(request):
    serializer = StudentEnrollmentSerializer(data=request.data, many=False)
    if serializer.is_valid():
        student_enrollment = StudentEnrollment.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

#update enrollment
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateStudentEnrollment(request,id):
    serializer= StudentEnrollmentSerializer(data=request.data, many=False)
    if serializer.is_valid():
        enrollment= StudentEnrollment.objects.get(id=id)
        enrollment.enrolled_student = Student.objects.get(id=request.data['enrolled_student'])
        enrollment.enrolled_class= Class.objects.get(id=request.data['enrolled_class'])
        enrollment.enrollTime = request.data['enrollTime']
        enrollment.gradeTime= request.data['gradeTime']
        enrollment.mark = request.data['mark']
        enrollment.save()
        return Response(serializer.data)

#lecturer and admin can change all students's marks
@api_view(['POST'])
@permission_classes([IsLecturer | IsAdminUser])
def enter_student_marks(request):
    """endpoint for entering student marks"""

    enrolment_id = request.data.get('enrolment_id')
    grade = request.data.get('grade')

    try:
        enrolment = StudentEnrollment.objects.get(id=enrolment_id)
        enrolment.grade = grade
        enrolment.save()
        serializer = StudentEnrollmentSerializer(enrolment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except StudentEnrollment.DoesNotExist:
        return Response({'error': 'Enrolment not found'}, status=status.HTTP_404_NOT_FOUND)


#student can only view his/her own marks
@api_view(['GET'])
@permission_classes([IsLecturer | IsStudent | IsAdminUser])
def view_student_marks(request, student_id):
    """endpoint for student to view his/her own marks"""
    if request.user.groups.filter(name="student").exists() and student_id != request.user.student_profile.id:
        return Response({'error': 'You are not authorized to view marks for this student.'},
                        status=status.HTTP_403_FORBIDDEN)

    enrolments = StudentEnrollment.objects.filter(enrolled_student_id=student_id)
    serializer = StudentEnrollmentSerializer(enrolments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#upload excel file and save to database
from openpyxl import load_workbook
@api_view(['POST'])
def uploadExcel(request):
    print(request, 12323213213 )
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES.get('file')
        wb = load_workbook(file)
        sheet = wb.worksheets[0]
        data = list(sheet.values)
        print(data)
        headers = data[0]
        for row in data[1:]:
            student= Student()
            is_row_invalid=False
        #     #to judge this row exists or not
            for col_idx, col_value in enumerate(row):
                if headers[col_idx]=="username" :
                    print(User.objects.filter(username=col_value).exists(),88888)
        #             # print(col_value,"doaisjdsaodjsaodij")
                    if col_value==None or User.objects.filter(username=col_value).exists():
                        is_row_invalid=True
                        break
        #     # print(is_row_exist,"1111111")
                    userData={}
                    studentData={}
                    if(not is_row_invalid):
                        for col_idx, col_value in enumerate(row):
                            if headers[col_idx]=="username":
                                userData["username"] = col_value
                                # print(username, 1999)
                            if headers[col_idx]=="email":
                                userData["email"] =col_value
                                # print(email, 2999)
                            if headers[col_idx]=="first_name":
                                userData['first_name'] = col_value
                                # print(first_name, 3999)
                            if headers[col_idx]=="last_name":
                                userData['last_name'] = col_value
                            if headers[col_idx]=="DOB":
                                studentData['DOB'] = col_value
                            if headers[col_idx]=="username":
                                studentData['username'] = col_value
                                # print(last_name, 4999)
                        print(userData, 7999)
                        user=User.objects.create(**userData)
                        # user=User.objects.create(username=username,password=("000000"),email=email,first_name=first_name,last_name=last_name)
                        token = Token.objects.create(user=user)
                        student_group = Group.objects.get(name='Student') 
                        user.groups.add(student_group)
                        serializer = StudentSerializer(data=studentData, many=False)
                        if serializer.is_valid():
                            student = Student.objects.create(user=user, **studentData)
    return Response("success")
    
    #send email
from django.core.mail import send_mail
from django.contrib import messages

def send_email(req, id):
    studentEnroll = StudentEnrollment.objects.filter(id=id).first()
    
    if not studentEnroll:
        messages.error("there is no this student")
        return HttpResponse("there is no this student")
    student_email = studentEnroll.enrolled_student.email
    subject = "Your Grade is Available"
    message = f"Dear {studentEnroll.enrolled_student},\n\nYour grade for {studentEnroll.mark} is now available. "
    from_email = None  # Uses the default email in settings.py

    try:
        send_mail(subject, message, from_email, [student_email])
        messages.success(req, f"Email sent to {studentEnroll}.")
    except Exception as e:
        messages.error(req, str(e))
    
    return HttpResponse("Email has sent")


