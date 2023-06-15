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
    user_data = request.data.pop('user')
    user = User.objects.create(**user_data)
    print(user,"This is user")
    token = Token.objects.create(user=user)
    student_group = Group.objects.get(name='Student') 
    user.groups.add(student_group)
    serializer = StudentSerializer(data=request.data, many=False)
    student = Student.objects.create(user=user, **request.data)
    if(serializer.is_valid()):
        # serializer.save()
        return Response(serializer.data)
    else:
        user.delete()  # 如果保存失败，删除已创建的用户对象
        student.delete()  # 如果保存失败，删除已创建的学生对象
        return Response(serializer.errors)
 
@api_view(['POST'])
@permission_classes([IsAdminUser,IsAuthorOrReadOnly])
def createLecturer(request):
    # data = JSONParser().parse(request)
    user_data = request.data.pop('user')
    # print(user_data)
    user = User.objects.create(**user_data)
    token = Token.objects.create(user=user)
    lecturer_group = Group.objects.get(name='Lecturer') 
    # print(lecturer_group)
    user.groups.add(lecturer_group)
    serializer = LecturerSerializer(data=request.data, many=False)
    if serializer.is_valid():
        # serializer.save()
        lecturer = Lecturer.objects.create(user=user, **request.data)

        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def createSemester(request):
    serializer = SemesterSerializer(data=request.data, many=False)
    if serializer.is_valid():
        # serializer.save()
        semester = Semester.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def createCourse(request):
    serializer = CourseSerializer(data=request.data, many=False)
    if serializer.is_valid():
        course = Course.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def createClass(request):
    serializer = ClassSerializer(data=request.data, many=False)
    if serializer.is_valid():
        class_ = Class.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def createStudentEnrollment(request):
    serializer = StudentEnrollmentSerializer(data=request.data, many=False)
    if serializer.is_valid():
        student_enrollment = StudentEnrollment.objects.create(**request.data)
        return Response(serializer.data)
    return Response(serializer.errors)


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
    