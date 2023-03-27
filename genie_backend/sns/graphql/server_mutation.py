import graphene
from sns.graphql.schema import ServerType
from sns.models import Server, SNS


class CreateServer(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        server_name = graphene.String(required=True)
        sns_name = graphene.String(required=True)

    def mutate(self, info, server_name, sns_name):
        server_name = server_name.strip()
        sns = SNS.get_by_name(sns_name)

        try:
            server = Server(name=server_name, sns=sns)
            server.save()
        except Exception as e:
            # Need Revise
            print(e)

        return CreateServer(success=True)

'''
class RemoveWallet(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        wallet_address = graphene.String(required=True)

    @check_authenticate
    def mutate(self, info, network_name, wallet_address):
        user = info.context.user
        network = Network.get_by_title(network_name.strip())
        wallet = Wallet.get_wallet(user=user, network=network, address=wallet_address.strip())

        wallet.delete()

        return RemoveWallet(success=True)
'''

class ServerMutation(graphene.ObjectType):
    create_server = CreateServer.Field()
    
