import strawberry.django
from communities.models import Community
from users.models import User
from posts.models import Post
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


@strawberry.django.type(Community)
class CommunityType:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    creator: UserType
    posts: list[PostType]


@strawberry.django.type(PostVote)
class PostVoteType:
    value: strawberry.auto
    user: UserType
    post: PostType
