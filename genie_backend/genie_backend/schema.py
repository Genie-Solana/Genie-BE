import graphene

from sns.graphql.server_query import ServerQuery
from blockchain.graphql.wallet_mutation import WalletMutation

class Query(
    ServerQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    WalletMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
        )
