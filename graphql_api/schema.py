import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Wellcome to regreddit!"

schema = strawberry.Schema(query=Query)