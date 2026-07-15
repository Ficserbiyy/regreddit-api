import strawberry
from django.shortcuts import get_object_or_404
from communities.models import Community
from posts.models import Post
from .types import CommunityType, PostType
from .mutations import Mutation


@strawberry.type
class Query:

    @strawberry.field
    def communities(self) -> list[CommunityType]:
        ''' List all existing communities '''
        return Community.objects.all()                         # type: ignore

    @strawberry.field
    def community(
        self,
        id: int | None = None,
        name: str | None = None,
    ) -> CommunityType:

        if id:
            return get_object_or_404(Community, pk=id)         # type: ignore
        if name:
            return get_object_or_404(Community, name=name)     # type: ignore

        raise ValueError("Either 'id' or 'name' must be provided.")

    @strawberry.field
    def posts(self) -> list[PostType]:
        return Post.objects.all()                              # type: ignore


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
