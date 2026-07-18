from strawberry import Info
from exceptions import AuthenticationError
from .models import User


def get_current_user(info: Info) -> User:

    user = info.context.request.user
    if not user.is_authenticated:
        raise AuthenticationError("Authentication required.")
    return user