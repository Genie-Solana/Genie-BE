import graphene
from accounts.models import SocialAccount
from blockchain.models import Wallet, Network, WalletTransactionHistory
from sns.models import SNS, SNSConnectionInfo
from genie_backend.utils import errors


class RegisterWallet(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        tx_hash = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        sns_name: str,
        discriminator: str,
        network_name: str,
        address: str,
        tx_hash: str,
    ) -> "RegisterWallet":
        _sns_name: str = sns_name.strip()
        _discriminator: str = discriminator.strip()
        _network_name: str = network_name.strip()
        _address: str = address.strip()
        _tx_hash: str = tx_hash.strip()

        sns: "SNS" = SNS.get_by_name(_sns_name)
        network: "Network" = Network.get_by_name(_network_name)
        account: "SocialAccount" = SNSConnectionInfo.get_account(sns, _discriminator)

        try:
            Wallet.objects.create(network=network, account=account, address=_address)
            WalletTransactionHistory.objects.create(account=account, wallet_address=_address, tx_hash=_tx_hash, register_type="REGISTER")
        except Exception:
            raise errors.RegisterWalletFailure from Exception

        return RegisterWallet(success=True)


class UnregisterWallet(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        tx_hash = graphene.String(required=True)

    def mutate(
        self, info: graphene.ResolveInfo, network_name: str, address: str, tx_hash:str
    ) -> "UnregisterWallet":
        _network_name: str = network_name.strip()
        _address: str = address.strip()
        _tx_hash: str = tx_hash

        network: "Network" = Network.get_by_name(_network_name)
        wallet: "Wallet" = Wallet.get_by_network_address(network, _address)

        wallet.delete()
        WalletTransactionHistory.objects.create(account=wallet.account, wallet_address=_address, tx_hash=_tx_hash, register_type="UNREGISTER")

        return UnregisterWallet(success=True)


class WalletMutation(graphene.ObjectType):
    register_wallet = RegisterWallet.Field()
    unregister_wallet = UnregisterWallet.Field()
