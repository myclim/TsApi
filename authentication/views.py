from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import UserModel
from authentication.utils import gen_jwt



class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = UserModel.objects.get(email=email)

            if user.get_password(password=password):
                token = gen_jwt(user)
                return Response({"token": token})
            
    
class UserRegisterView(APIView):
    def post(self, request):

        data = request.data

        if data["password1"] != data["password2"]:
            return Response({"error": "Пароли не совпадают"})

        if UserModel.objects.filter(email=data["email"]).exists():
            return Response({"error": "Пользователь с таким email уже существует"})

        user = UserModel(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data["middle_name"],
            email=data["email"],
        )
        user.set_password(data["password1"])
        user.save()

        return Response({"message": "Пользователь успешно зарегистрирован"})


class DeleteAccountView(APIView):

    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user
            user.delete_user()
            return Response({"message": "Пользователь удалян"}, status=200)
        else:
            return Response({"error": "Требуется авторизация"}, status=401)
