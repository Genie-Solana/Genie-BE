import requests
import graphene
from django.core.files.base import ContentFile
from sns.models import SNS, SNSConnectionInfo
from blockchain.models import Network
from accounts.models import SocialAccount
from genie_backend.utils import errors


class RegisterSNS(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        handle = graphene.String(required=True)
        profile_img = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        network_name: str,
        address: str,
        sns_name: str,
        discriminator: str,
        handle: str,
        profile_img,
    ) -> graphene.Mutation:
        _network_name: str = network_name.strip()
        _address: str = address.strip()
        _sns_name: str = sns_name.strip()
        _discriminator: str = discriminator.strip()
        _handle: str = handle.strip()
            
        try:
            response = requests.get(profile_img)
            image_content = response.content
            profile_img = ContentFile(image_content, f'{_sns_name}{_discriminator}.png')
        except:
            profile_img = None

        network: "Network" = Network.get_by_name(_network_name)
        sns: "SNS" = SNS.get_by_name(_sns_name)
        account: "SocialAccount" = SocialAccount.get_by_pub_key(_address)

        try:
            SNSConnectionInfo.objects.create(
                account=account, sns=sns, discriminator=_discriminator, handle=_handle, profile_img=profile_img
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
        discriminator = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        network_name: str,
        address: str,
        sns_name: str,
        discriminator: str,
    ) -> graphene.Mutation:
        _network_name: str = network_name.strip()
        _address: str = address.strip()
        _sns_name: str = sns_name.strip()
        _discriminator: str = discriminator.strip()

        network: "Network" = Network.get_by_name(_network_name)
        sns: "SNS" = SNS.get_by_name(_sns_name)
        account: "SocialAccount" = SocialAccount.get_by_pub_key(_address)

        sns_connection: "SNSConnectionInfo" = SNSConnectionInfo.get_sns_connection(
            sns=sns, account=account, discriminator=_discriminator
        )

        sns_connection.delete()

        return UnregisterSNS(success=True)


class SNSMutation(graphene.ObjectType):
    register_sns = RegisterSNS.Field()
    unregister_sns = UnregisterSNS.Field()
