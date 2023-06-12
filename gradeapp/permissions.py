from rest_framework import permissions

# 如果请求的方法属于安全方法（例如 GET、HEAD、OPTIONS），has_object_permission 方法返回 True，表示允许所有用户进行只读操作。

# 如果请求的方法不属于安全方法（例如 POST、PUT、DELETE），has_object_permission 方法会比较对象的作者（obj.author）和请求的用户（request.user）。如果二者匹配，表示该用户是对象的作者，返回 True，表示允许用户进行修改操作。否则，返回 False，表示不允许用户进行修改操作。
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print("object author", obj.author)
        print("request user", request.user)
        return obj.author == request.user