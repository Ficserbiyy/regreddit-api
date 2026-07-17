import strawberry


@strawberry.input
class CommunityInput:
    name: str
    description: str

@strawberry.input
class UserInput:
    username: str
    email: str
    password: str

@strawberry.input
class LoginInput:
    username: str
    password: str
