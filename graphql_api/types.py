import strawberry.django
from strawberry import Info
from django.db.models import Sum
from communities.models import Community
from users.models import User
from posts.models import Post
from comments.models import Comment
from votes.models import PostVote, CommentVote


@strawberry.django.type(User)
class UserType:
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto


@strawberry.django.type(Post)
class PostType:
    id: strawberry.auto
    title: strawberry.auto
    creator: UserType
    @strawberry.field
    def score(self) -> int:
        return (
            PostVote.objects.filter(post=self)
            .aggregate(score=Sum("value"))["score"]
            or 0
        )
    @strawberry.field
    def vote_status(
        self,
        info: Info,
    ) -> int:
        user = info.context.request.user
        if not user.is_authenticated:
            return 0
        vote = PostVote.objects.filter(
            post=self,
            user=user,
        ).first()
        return vote.value if vote else 0


@strawberry.django.type(Comment)
class CommentType:
    id: strawberry.auto
    body: strawberry.auto
    creator: UserType
    post: PostType
    @strawberry.field
    def score(self) -> int:
        return (
            CommentVote.objects.filter(comment=self)
            .aggregate(score=Sum("value"))["score"]
            or 0
        )
    @strawberry.field
    def vote_status(
        self,
        info: Info,
    ) -> int:
        user = info.context.request.user
        if not user.is_authenticated:
            return 0
        vote = CommentVote.objects.filter(
            post=self,
            user=user,
        ).first()
        return vote.value if vote else 0


@strawberry.django.type(Community)
class CommunityType:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    creator: UserType
    posts: list[PostType]


@strawberry.type
class PostPage:
    items: list[PostType]
    page: int
    limit: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


@strawberry.type
class CommentPage:
    items: list[CommentType]
    page: int
    limit: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


@strawberry.type
class CommunityPage:
    items: list[CommunityType]
    page: int
    limit: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool
