import graphene
from accounts.models import SocialAccount, Inbox
from sns.models import SNS, SNSConnectionInfo
from blockchain.models import Network
from genie_backend.utils.api_calls import create_social_account_call, create_inbox_account_call
from genie_backend.utils import errors


class CreateSocialAccount(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        nickname = graphene.String(required=True)

    def mutate(self, info, nickname):
        nickname = nickname.strip()
        data, sec_key = create_social_account_call()
        pub_key = data['data']['social_account_key']
        SocialAccount.objects.create(
            nickname=nickname,
            pub_key=pub_key,
            secret_key=sec_key,
        )
        return CreateSocialAccount(success=True)


class CreateInboxAccount(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)
        network_name = graphene.String(required=True)

    def mutate(self, info, sns_name, handle, network_name):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, handle)
        network = Network.get_by_name(network_name)
        data, sec_key = create_inbox_account_call(sns_name.lower(), handle)
        pub_key = data['data']['inbox_key']
        Inbox.objects.create(
            pub_key=pub_key,
            secret_key=sec_key,
            account=account,
            network=network,
            sns=sns,
        )
        return CreateInboxAccount(success=True)


class AccountMutation(graphene.ObjectType):
    create_social_account = CreateSocialAccount.Field()
    create_inbox_account = CreateInboxAccount.Field()