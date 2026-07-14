import strawberry
from communities.models import Community
from posts.models import Post
from .types import CommunityType, PostType


@strawberry.type
class Query:

    @strawberry.field
    def communities(self) -> list[CommunityType]:
        return Community.objects.all()  # type: ignore
    
    @strawberry.field
    def posts(self) -> list[PostType]:
        return Post.objects.all()       # type: ignore

schema = strawberry.Schema(query=Query)
