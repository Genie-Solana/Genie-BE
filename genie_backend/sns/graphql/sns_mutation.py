import graphene
from sns.models import SNS, SNSConnectionInfo
from blockchain.models import Wallet, Network
from accounts.models import SocialAccount
from genie_backend.utils import errors


class RegisterSNS(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)
        # profile_img = graphene ~~~

    def mutate(
        self,
        info: graphene.ResolveInfo,
        network_name: str,
        address: str,
        sns_name: str,
        handle: str,
        profile_img=None,
    ) -> graphene.Mutation:
        _network_name: str = network_name.strip()
        _address: str = address.strip()
        _sns_name: str = sns_name.strip()
        _handle: str = handle.strip()

        network: "Network" = Network.get_by_name(_network_name)
        sns: "SNS" = SNS.get_by_name(_sns_name)
        wallet: "Wallet" = Wallet.get_by_network_address(network, _address)
        account: "SocialAccount" = wallet.account

        try:
            SNSConnectionInfo.objects.create(
                account=account, sns=sns, handle=_handle, profile_img=profile_img
            )
        except Exception:
            raise errors.RegisterSNSFailure from Exception

        return RegisterSNS(success=True)


class UnregisterSNS(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        network_name: str,
        address: str,
        sns_name: str,
        handle: str,
    ) -> graphene.Mutation:
        _network_name: str = network_name.strip()
        _address: str = address.strip()
        _sns_name: str = sns_name.strip()
        _handle: str = handle.strip()

        network: "Network" = Network.get_by_name(_network_name)
        sns: "SNS" = SNS.get_by_name(_sns_name)
        wallet: "Wallet" = Wallet.get_by_network_address(network, _address)
        account: "SocialAccount" = wallet.account

        sns_connection: "SNSConnectionInfo" = SNSConnectionInfo.get_sns_connection(
            sns=sns, account=account, handle=_handle
        )

        sns_connection.delete()

        return UnregisterSNS(success=True)


class SNSMutation(graphene.ObjectType):
    register_sns = RegisterSNS.Field()
    unregister_sns = UnregisterSNS.Field()
