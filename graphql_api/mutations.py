import strawberry
from strawberry import Info
from communities.models import Community
from posts.models import Post
from comments.models import Comment
from votes.models import PostVote, CommentVote, VoteValue
from users.models import User
from exceptions import AuthenticationError, ValidationError, NotFoundError
from .types import CommunityType, UserType, CommentType, PostType
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
    def upvote_post(
        self,
        info: Info,
        post_id: int,
    ) -> PostType | None:
        current_user = get_current_user(info)
        db_post = Post.objects.filter(pk=post_id).first()
        if not db_post:
            raise NotFoundError("Post not found")

        existing_vote = PostVote.objects.filter(user=current_user, post=db_post).first()
        if not existing_vote:
            PostVote.objects.create(
                user = current_user,
                post = db_post,
                value = VoteValue.UP,
            )
            return db_post                      # type: ignore            

        if existing_vote.value == VoteValue.DOWN:
            existing_vote.value = VoteValue.UP
            existing_vote.save()
            return db_post                      # type: ignore
        else:
            existing_vote.delete()
            return None


    @strawberry.mutation
    def downvote_post(
        self,
        info: Info,
        post_id: int,
    ) -> PostType | None:
        current_user = get_current_user(info)
        db_post = Post.objects.filter(pk=post_id).first()
        if not db_post:
            raise NotFoundError("Post not found")

        existing_vote = PostVote.objects.filter(user=current_user, post=db_post).first()
        if not existing_vote:
            PostVote.objects.create(
                user = current_user,
                post = db_post,
                value = VoteValue.DOWN,
            )
            return db_post                      # type: ignore

        if existing_vote.value == VoteValue.UP:
            existing_vote.value = VoteValue.DOWN
            existing_vote.save()
            return db_post                      # type: ignore
        else:
            existing_vote.delete()
            return None


    @strawberry.mutation
    def upvote_comment(
        self,
        info: Info,
        comment_id: int,
    ) -> CommentType | None:
        current_user = get_current_user(info)
        db_comment = Comment.objects.filter(pk=comment_id).first()
        if not db_comment:
            raise NotFoundError("Comment not found")

        existing_vote = CommentVote.objects.filter(user=current_user, comment=db_comment).first()
        if not existing_vote:
            CommentVote.objects.create(
                user = current_user,
                comment = db_comment,
                value = VoteValue.UP,
            )
            return db_comment                   # type: ignore

        if existing_vote.value == VoteValue.DOWN:
            existing_vote.value = VoteValue.UP
            existing_vote.save()
            return db_comment                   # type: ignore
        else:
            existing_vote.delete()
            return None


    @strawberry.mutation
    def downvote_comment(
        self,
        info: Info,
        comment_id: int,
    ) -> CommentType | None:
        current_user = get_current_user(info)
        db_comment = Comment.objects.filter(pk=comment_id).first()
        if not db_comment:
            raise NotFoundError("Comment not found")

        existing_vote = CommentVote.objects.filter(user=current_user, comment=db_comment).first()
        if not existing_vote:
            CommentVote.objects.create(
                user = current_user,
                comment = db_comment,
                value = VoteValue.DOWN,
            )
            return db_comment                   # type: ignore

        if existing_vote.value == VoteValue.UP:
            existing_vote.value = VoteValue.DOWN
            existing_vote.save()
            return db_comment                   # type: ignore
        else:
            existing_vote.delete()
            return None


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
