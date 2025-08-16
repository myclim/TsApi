from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.permissions import UserCustomPermission


class ResourceView(APIView):
    permission_classes = [UserCustomPermission]

    def get(self, request):
        self.required_permission = "view"
        self.check_permissions(request)
        return Response({"message": "GET доступен"})

    def post(self, request):
        self.required_permission = "create"
        self.check_permissions(request)
        return Response({"message": "POST (создание) доступно"})

    def put(self, request):
        self.required_permission = "update"
        self.check_permissions(request)
        return Response({"message": "PUT (обновление) доступно"})

    def delete(self, request):
        self.required_permission = "delete"
        self.check_permissions(request)
        return Response({"message": "DELETE доступен"})
