from typing import Optional
import graphene
from django.db.models import QuerySet
from accounts.graphql.schema import GetAccountInfoReturnType
from sns.models import SNS, SNSConnectionInfo
from genie_backend.utils import errors


class AccountQuery(graphene.ObjectType):
    get_social_account_info = graphene.NonNull(
        GetAccountInfoReturnType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
    )

    def resolve_get_social_account_info(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        handle = kwargs.get("discriminator")
        
        try:
            sns = SNS.get_by_name(sns_name)
            social_account = SNSConnectionInfo.get_account(sns, discriminator)
        except:
            raise errors.AccountNotFound

        return GetAccountInfoReturnType(success=True, pub_key=social_account.pub_key, nickname=social_account.nickname)
