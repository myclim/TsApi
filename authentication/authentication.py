from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from authentication.utils import decode_jwt
from authentication.models import UserModel


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]
        elif "jwt" in request.COOKIES:
            token = request.COOKIES.get("jwt")
        else:
            return None

        payload = decode_jwt(token)
        if not payload:
            raise AuthenticationFailed("Неверный или истёкший токен")

        try:
            user = UserModel.objects.get(id=payload["user_id"], is_active=True)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed("Пользователь не найден")

        return (user, None)
