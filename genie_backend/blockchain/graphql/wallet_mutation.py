import graphene
from accounts.models import SocialAccount
from blockchain.models import Wallet, Network
from sns.models import SNS, SNSConnectionInfo
from genie_backend.utils import errors


class RegisterWallet(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        sns_name: str,
        handle: str,
        network_name: str,
        address: str,
    ) -> "RegisterWallet":
        _sns_name: str = sns_name.strip()
        _handle: str = handle.strip()
        _network_name: str = network_name.strip()
        _address: str = address.strip()

        sns: "SNS" = SNS.get_by_name(_sns_name)
        network: "Network" = Network.get_by_name(_network_name)
        account: "SocialAccount" = SNSConnectionInfo.get_account(sns, _handle)

        try:
            Wallet.objects.create(network=network, account=account, address=_address)
        except Exception:
            raise errors.RegisterWalletFailure from Exception

        return RegisterWallet(success=True)


class UnregisterWallet(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)

    def mutate(
        self, info: graphene.ResolveInfo, network_name: str, address: str
    ) -> "UnregisterWallet":
        _network_name: str = network_name.strip()
        _address: str = address.strip()

        network: "Network" = Network.get_by_name(_network_name)
        wallet: "Wallet" = Wallet.get_by_network_address(network, _address)

        wallet.delete()

        return UnregisterWallet(success=True)


class WalletMutation(graphene.ObjectType):
    register_wallet = RegisterWallet.Field()
    unregister_wallet = UnregisterWallet.Field()
