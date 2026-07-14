import strawberry
from communities.models import Community
from .types import CommunityType


@strawberry.type
class Query:

    @strawberry.field
    def communities(self) -> list[CommunityType]:
        return Community.objects.all()  # type: ignore


schema = strawberry.Schema(query=Query)
