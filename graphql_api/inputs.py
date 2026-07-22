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

@strawberry.input
class CommunityFilter:
    name: str | None = None
    creator: str | None = None
    page: int = 1
    limit: int = 20

@strawberry.input
class PostFilter:
    community: str | None = None
    creator: str | None = None
    sort_by: str = "score_desc"
    page: int = 1
    limit: int = 20

@strawberry.input
class CommentFilter:
    post: int | None = None
    creator: str | None = None
    sort_by: str = "score_desc"
    page: int = 1
    limit: int = 20
