import strawberry
from strawberry import Info
from communities.models import Community
from users.models import User
from .types import CommunityType, CommunityInput, UserType, UserInput, LoginInput
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
        
        user = info.context.request.user
        if not user.is_authenticated:
            raise ValueError("Authentication required.")

        community = Community.objects.create(
            name=data.name,
            description=data.description,
            owner = user
        )
        return community                        # type: ignore


    @strawberry.mutation
    def register(
        self,
        data: UserInput,
    ):
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
        )
        return user


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
            raise ValueError("Invalid username or password.")
        auth_login(info.context.request, user)
        return user                             # type: ignore


    @strawberry.mutation
    def logout(
        self,
        info: Info,
    ):
        auth_logout(info.context.request)
        return True


    @strawberry.field
    def me(
        self,
        info: Info
    ) -> UserType | None:
        
        user = info.context.request.user
        if not user.is_authenticated:
            return None
        return user
