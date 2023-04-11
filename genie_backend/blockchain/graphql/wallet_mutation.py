import graphene
from blockchain.graphql.schema import WalletType
from blockchain.models import Wallet, Network
from sns.models import SNS, SNSConnectionInfo
from genie_backend.utils import errors


class RegisterWallet(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)

    def mutate(self, info, sns_name, handle, network_name, address):
        sns_name = sns_name.strip()
        handle = handle.strip()
        network_name = network_name.strip()
        address = address.strip()

        sns = SNS.get_by_name(sns_name)
        network = Network.get_by_name(network_name)
        account = SNSConnectionInfo.get_account(sns, handle)

        try:
            Wallet.objects.create(network=network, account=account, address=address)
        except Exception:
            raise errors.RegisterWalletFailure

        return RegisterWallet(success=True)


class UnregisterWallet(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)

    def mutate(self, info, network_name, address):
        network_name = network_name.strip()
        address = address.strip()
        
        network = Network.get_by_name(network_name)
        wallet = Wallet.get_by_network_address(network, address)
        
        wallet.delete()
        
        return UnregisterWallet(success=True)


class WalletMutation(graphene.ObjectType):
    register_wallet = RegisterWallet.Field()
    unregister_wallet = UnregisterWallet.Field()
