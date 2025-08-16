from django.utils.deprecation import MiddlewareMixin

from authentication.utils import decode_jwt
from authentication.models import UserModel


class JwtMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.user:
            token = request.headers.get("Authorization")

            if token and token.startswith("Bearer "):
                token = token.split(" ")[1]

                data_token = decode_jwt(token)

                if data_token:
                    user = UserModel.objects.get(
                        id=data_token["user_id"], is_active=True
                    )
                    request.user = user
