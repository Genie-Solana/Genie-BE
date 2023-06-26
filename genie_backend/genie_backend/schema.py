import graphene

from accounts.graphql.user_query import AccountQuery
from sns.graphql.server_query import ServerQuery
from blockchain.graphql.wallet_mutation import WalletMutation
from sns.graphql.server_mutation import ServerMutation
from sns.graphql.sns_mutation import SNSMutation


class Query(
    AccountQuery,
    ServerQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    WalletMutation,
    ServerMutation,
    SNSMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
        )
