import strawberry
from communities.models import Community
from .types import CommunityType, CommunityInput


@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def create_community(
        self,
        data: CommunityInput,
    ) -> CommunityType:
        community = Community.objects.create(
            name=data.name,
            description=data.description,
        )
        return community                        # type: ignore

