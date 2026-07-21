import strawberry.django
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


@strawberry.django.type(Comment)
class CommentType:
    id: strawberry.auto
    creator: UserType
    post: PostType
    @strawberry.field
    def score(self) -> int:
        return (
            CommentVote.objects.filter(comment=self)
            .aggregate(score=Sum("value"))["score"]
            or 0
        )


@strawberry.django.type(Community)
class CommunityType:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    creator: UserType
    posts: list[PostType]
