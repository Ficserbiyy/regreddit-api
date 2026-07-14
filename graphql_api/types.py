import strawberry.django
from communities.models import Community


@strawberry.django.type(Community)
class CommunityType:
    id: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
