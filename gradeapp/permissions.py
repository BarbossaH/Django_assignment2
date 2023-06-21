from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):   
        if request.method in permissions.SAFE_METHODS:
            print("object author", obj)
            print("request user", request)  
            return True        
        return False
    
# class IsLecturer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name="Lecturer").exists()

#     def has_object_permission(self, request, view, obj):
#         if request.method == 'PATCH':
#             if set(request.data.keys()) <= {'grade'}:
#                 return True
#         return False


# class IsStudent(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name="Student").exists()

#     def has_object_permission(self, request, view, obj):
#         if request.method == 'GET':
#             return obj.enrolled_student.user == request.user

#         return False