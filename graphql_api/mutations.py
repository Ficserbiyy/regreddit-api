import strawberry
from strawberry import Info
from communities.models import Community
from users.models import User
from exceptions import AuthenticationError, ValidationError
from .types import CommunityType, UserType
from .inputs import CommunityInput, UserInput, LoginInput
from users.helprers import get_current_user
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)


@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def create_community(
        self,
        info: Info,
        data: CommunityInput,
    ) -> CommunityType:
        user = get_current_user(info)
        if Community.objects.filter(name=data.name).exists():
            raise ValidationError(f"Community '{data.name}' already exists.")

        community = Community.objects.create(
            name=data.name,
            description=data.description,
            creator = user
        )
        return community                        # type: ignore


    @strawberry.mutation
    def register(
        self,
        data: UserInput,
    ) -> UserType:

        if User.objects.filter(username=data.username).exists():
            raise AuthenticationError("Username already exists.")
        if User.objects.filter(email=data.email).exists():
            raise AuthenticationError("Email already registered.")

        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
        )
        return user                             # type: ignore


    @strawberry.mutation
    def login(
        self,
        info: Info,
        data: LoginInput,
    ) -> UserType:
        user = authenticate(
            username=data.username,
            password=data.password,
        )
        if not user:
            raise AuthenticationError("Invalid username or password.")
        auth_login(info.context.request, user)
        return user                             # type: ignore


    @strawberry.mutation
    def logout(
        self,
        info: Info,
    ) -> bool:
        auth_logout(info.context.request)
        return True
