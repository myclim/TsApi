import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from django.conf import settings


def gen_jwt(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp()),
        "role": user.role.id,
    }
    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None
