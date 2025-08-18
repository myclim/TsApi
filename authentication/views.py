from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from authentication.utils import gen_jwt
from authentication.models import (
    RoleModel,
    RolePermissionModel,
    PermissionModel,
    UserModel,
)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "email и пароль обязательны"}, status=400)

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response(
                {"error": "Пользователь с таким email не найден"}, status=404
            )

        if not user.get_password(password=password):
            return Response({"error": "Неверный пароль"}, status=401)

        token = gen_jwt(user)
        responce = Response({"message": "Успешный вход", "token": token}, status=200)

        responce.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=False,
            samesite="Strict",
            max_age=24 * 3600,
        )
        return responce


class UserLogoutView(APIView):
    def post(self):
        responce = Response({"message": "Успешный выход"}, status=200)
        responce.delete_cookie("jwt")
        return responce


class UserRegisterView(APIView):
    def post(self, request):

        data = request.data

        if data["password1"] != data["password2"]:
            return Response({"error": "Пароли не совпадают"}, status=400)

        if UserModel.objects.filter(email=data["email"]).exists():
            return Response(
                {"error": "Пользователь с таким email уже существует"}, status=400
            )

        if data.get("role"):
            role = RoleModel.objects.get(name=data["role"])
        else:
            role = RoleModel.objects.get(name="guest")

        user = UserModel(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data["middle_name"],
            email=data["email"],
            role=role,
        )
        user.set_password(data["password1"])
        user.save()

        return Response({"message": "Пользователь успешно зарегистрирован"}, status=201)


class UserUpdateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Нужна авторизация"}, status=401)

        user = request.user
        data = request.data
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.middle_name = data.get("middle_name", user.middle_name)
        user.email = data.get("email", user.email)
        user.save()
        return Response({"message": "Профиль обновлен"}, status=200)


class UserDeleteView(APIView):

    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user
            user.delete_user()
            response = Response({"message": "Успешное удаление"}, status=200)
            response.delete_cookie("jwt")
            return response
        else:
            return Response({"error": "Требуется авторизация"}, status=401)


class RolePermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role.name != "admin":
            return Response({"error": "Только для admin"}, status=403)

        roles = RoleModel.objects.all()
        data = []
        for role in roles:
            action = RolePermissionModel.objects.filter(role=role).values_list(
                "permission__name"
            )
            data.append({"role": role.name, "permission": [i[0] for i in action]})

        return Response(data, status=200)

    def post(self, request):
        if request.user.role.name != "admin":
            return Response({"error": "Только для admin"}, status=403)

        role_name = request.data.get("role")
        permissions = request.data.get("permissions", [])

        role = get_object_or_404(RoleModel, name=role_name)
        RolePermissionModel.objects.filter(role=role).delete()

        for list_item in permissions:
            perm = get_object_or_404(PermissionModel, name=list_item)
            RolePermissionModel.objects.create(role=role, permission=perm)

        return Response(
            {"message": f"Права для роли {role.name} обновлены"}, status=200
        )
