import graphene

from sns.graphql.server_query import ServerQuery
from sns.graphql.server_mutation import ServerMutation
from sns.graphql.sns_mutation import SNSMutation


class Query(
    ServerQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    ServerMutation,
    SNSMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
        )
