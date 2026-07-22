import strawberry
from strawberry import Info
from communities.models import Community
from posts.models import Post
from comments.models import Comment
from exceptions import ValidationError, NotFoundError
from utils.validators import validate_query_pagination
from .types import CommunityType, PostType, UserType, CommentType
from .inputs import CommentFilter, PostFilter, CommunityFilter


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
    def communities(
        self,
        filters: CommunityFilter,
    ) -> list[CommunityType]:
        validate_query_pagination(filters)
        queryset = Community.objects.all()

        if filters.name:
            queryset = queryset.filter(
                name__icontains=filters.name    # Case-insensitive substring search.
            )
        if filters.creator:
            queryset = queryset.filter(
                creator__username=filters.creator
            )
        offset = (filters.page - 1) * filters.limit
        return queryset[offset:offset + filters.limit]         # type: ignore


    @strawberry.field
    def posts(
        self,
        filters: PostFilter,
    ) -> list[PostType]:
        validate_query_pagination(filters)
        queryset = Post.objects.all()

        if filters.community:
            queryset = queryset.filter(
                community__name=filters.community
            )
        if filters.creator:
            queryset = queryset.filter(
                creator__username=filters.creator
            )
        match filters.sort_by:
            case "newest":
                queryset = queryset.order_by("-created_at")
            case "oldest":
                queryset = queryset.order_by("created_at")
            case "score_asc":
                queryset = queryset.order_by("score")
            case _:
                queryset = queryset.order_by("-score")
            
        offset = (filters.page - 1) * filters.limit
        return queryset[offset:offset + filters.limit]         # type: ignore


    @strawberry.field
    def comments(
        self,
        filters: CommentFilter
    ) -> list[CommentType]:
        validate_query_pagination(filters)
        queryset = Comment.objects.all()

        if filters.post:
            queryset = queryset.filter(
                post_id=filters.post
            )
        if filters.creator:
            queryset = queryset.filter(
                creator__username=filters.creator
            )
        match filters.sort_by:
            case "newest":
                queryset = queryset.order_by("-created_at")
            case "oldest":
                queryset = queryset.order_by("created_at")
            case "score_asc":
                queryset = queryset.order_by("score")
            case _:
                queryset = queryset.order_by("-score")
            
        offset = (filters.page - 1) * filters.limit
        return queryset[offset:offset + filters.limit]         # type: ignore


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
