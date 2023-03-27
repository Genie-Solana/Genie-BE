import graphene
from sns.graphql.schema import ServerType
from sns.models import Server


class CreateServer(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        server_name = graphene.String(required=True)
        server_sns = graphene.String()

    def mutate(self, info, server_name, server_sns=None):
        server_name = server_name.strip()

        try:
            server = Server(name=server_name, sns=server_sns)
            server.save()
        except Exception:
            # Need Revise
            print('CreateServerError')

        return CreateServer(success=True)


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


class WalletMutation(graphene.ObjectType):
    add_wallet = AddWallet.Field()
    remove_wallet = RemoveWallet.Field()
