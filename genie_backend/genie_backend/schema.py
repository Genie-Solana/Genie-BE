import graphene

from sns.graphql.server_query import ServerQuery


class Query(
    ServerQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
        )
