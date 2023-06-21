from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from gradeapp.permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
# from gradeapp.models import Post
from gradeapp.serializers import StudentSerializer, LecturerSerializer,SemesterSerializer,CourseSerializer,ClassSerializer,StudentEnrollmentSerializer
from gradeapp.models import Student, Lecturer,Semester,Course,Class,StudentEnrollment


@api_view(['GET'])
def index(request):
    # if request.user.is_authenticated:
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

@api_view(['POST'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def createSemester(request):
    serializer = SemesterSerializer(data=request.data, many=False)
    if serializer.is_valid():
        # serializer.save()
        semester = Semester.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def updateSemester(request,id):
    serializer = SemesterSerializer(data=request.data, many=False)
    if serializer.is_valid():
        semester = Semester.objects.get(id=id)
        semester.year = request.data['year']
        semester.semester = request.data['semester']
        semester.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def createCourse(request):
    serializer = CourseSerializer(data=request.data, many=False)
    if serializer.is_valid():
        course = Course.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

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


@api_view(['POST'])
def createClass(request):
    serializer = ClassSerializer(data=request.data, many=False)
    if serializer.is_valid():
        class_ = Class.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def updateClass(request,id):
    serializer= ClassSerializer(data=request.data, many=False)
    if serializer.is_valid():
        class_ = Class.objects.get(id=id)
        class_.semester = request.data['name']
        class_.number = request.data['number']
        class_.course = Course.objects.get(id=request.data['course'])
        class_.save()
        return Response(serializer.data)



@api_view(['POST'])
def createStudentEnrollment(request):
    serializer = StudentEnrollmentSerializer(data=request.data, many=False)
    if serializer.is_valid():
        student_enrollment = StudentEnrollment.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def updateStudentEnrollment(request,id):
    serializer= StudentEnrollmentSerializer(data=request.data, many=False)
    if serializer.is_valid():
        enrollment= StudentEnrollment.objects.get(id=id)
        enrollment.enrolled_class = Student.objects.get(id=request.data['enrolled_class'])
        enrollment.enrolled_student = Class.objects.get(id=request.data['enrolled_student'])
        enrollment.enrollTime = request.data['enrollTime']
        enrollment.gradeTime= request.data['gradeTime']
        enrollment.save()
        return Response(serializer.data)

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
    