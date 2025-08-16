import jwt
from datetime import datetime, timedelta
from django.conf import settings



def gen_jwt(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'role': user.role.name if user.role else None,
    }
    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")


def decode_jwt(api_token):
    try:
        return jwt.decode(jwt=api_token, key=settings.SECRET_KEY, algorithms="HS256")
    except:
        return None

