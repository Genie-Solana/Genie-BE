import graphene

from sns.graphql.server_query import ServerQuery
from sns.graphql.server_mutation import ServerMutation


class Query(
    ServerQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    ServerMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
        )
