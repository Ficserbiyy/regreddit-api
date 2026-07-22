from strawberry import Schema
from .mutations import Mutation
from .queries import Query

schema = Schema(
    query=Query,
    mutation=Mutation
)
