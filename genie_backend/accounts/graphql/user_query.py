from typing import Optional
import graphene
from django.db.models import QuerySet
from accounts.models import Inbox
from accounts.graphql.schema import InboxType, GetAccountInfoReturnType, GetUserInfoReturnType, GetUserWalletAddressReturnType
from blockchain.models import Wallet, Network
from sns.models import SNS, SNSConnectionInfo
from genie_backend.utils import errors


class AccountQuery(graphene.ObjectType):
    get_social_account_info = graphene.NonNull(
        GetAccountInfoReturnType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
    )
    
    get_user_info = graphene.NonNull(
        GetUserInfoReturnType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
    )

    get_user_wallet_address = graphene.NonNull(
        GetUserWalletAddressReturnType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
    )

    def resolve_get_social_account_info(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")
        
        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)

        return GetAccountInfoReturnType(pub_key=social_account.pub_key, nickname=social_account.nickname)

    def resolve_get_user_info(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")

        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)
        sns_connection_info = SNSConnectionInfo.get_sns_connection(sns, social_account, discriminator)

        #sns_profile_img = sns_connection_info.profile_img
        sns_nickname = sns_connection_info.handle
        account_pub_key = social_account.pub_key
        account_nickname = social_account.nickname
        inbox_list = Inbox.objects.filter(account=social_account)

        return GetUserInfoReturnType(
            #sns_profile_img=sns_profile_img,
            sns_nickname=sns_nickname,
            account_pub_key=account_pub_key,
            account_nickname=account_nickname,
            inbox_list=inbox_list,
        )

    def resolve_get_user_wallet_address(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")

        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)
        
        wallet_list = Wallet.objects.filter(account=social_account)
        
        return GetUserWalletAddressReturnType(wallet_list=wallet_list)
        

