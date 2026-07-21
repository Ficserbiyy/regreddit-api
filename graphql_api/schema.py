import strawberry
from strawberry import Info
from communities.models import Community
from posts.models import Post
from comments.models import Comment
from exceptions import ValidationError, NotFoundError
from .types import CommunityType, PostType, UserType, CommentType
from .mutations import Mutation


@strawberry.type
class Query:

    @strawberry.field
    def me(
        self,
        info: Info
    ) -> UserType | None:
        
        user = info.context.request.user
        if not user.is_authenticated:
            return None
        return user


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

        if id is None and not name:
            raise ValidationError("Either 'id' or 'name' must be provided.")
        if id is not None and id <= 0:
            raise ValidationError("Community id must be greater than 0.")

        community = (
            Community.objects.filter(pk=id).first()
            if id is not None
            else Community.objects.filter(name=name).first()
        )
        if not community:
            raise NotFoundError("Community not found.")
        return community                                       # type: ignore


    @strawberry.field
    def posts(self) -> list[PostType]:
        ''' List all existing posts '''
        return Post.objects.all()                              # type: ignore


    @strawberry.field
    def comments(self) -> list[CommentType]:
        ''' List all existing comments '''
        return Comment.objects.all()                              # type: ignore


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
