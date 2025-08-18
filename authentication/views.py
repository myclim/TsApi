from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import UserModel, RoleModel
from authentication.utils import gen_jwt



class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'email и пароль обязательны'}, status=400)

        user = get_object_or_404(UserModel, email=email)
        if not user.get_password(password=password):
            return Response({'error': 'Неверный пароль'}, status=401)
        
        token = gen_jwt(user)
        responce = Response({'message': 'Успешный вход'}, status=200)

        responce.set_cookie(
            key='jwt',
            value=token,
            httponly=True,
            secure=False,
            samesite='Strict',
            max_age=24*3600
        )
        return responce
    

class UserRegisterView(APIView):
    def post(self, request):

        data = request.data

        if data["password1"] != data["password2"]:
            return Response({"error": "Пароли не совпадают"}, status=400)

        if UserModel.objects.filter(email=data["email"]).exists():
            return Response({"error": "Пользователь с таким email уже существует"}, status=400)
        
        if data.get('role'):
            role = RoleModel.objects.get(name=data['role'])
        else:
            role = RoleModel.objects.get(name='guest')

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
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.middle_name = data.get('middle_name', user.middle_name)
        user.email = data.get('email', user.email)
        user.save()
        return Response({'message': 'Профиль обновлен'}, status=200)
        


class UserDeleteView(APIView):

    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user
            user.delete_user()
            return Response({"message": "Пользователь удалян"}, status=200)
        else:
            return Response({"error": "Требуется авторизация"}, status=401)
