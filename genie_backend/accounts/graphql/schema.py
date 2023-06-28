import graphene
from accounts.models import SocialAccount, Inbox
from blockchain.models import Network
from graphene_django.types import DjangoObjectType


class NetworkType(DjangoObjectType):
    class Meta:
        model = Network
        fields = ("name",)


class InboxType(DjangoObjectType):
    class Meta:
        model = Inbox
        fields = ("pub_key", "network")


class GetAccountInfoReturnType(graphene.ObjectType):
    pub_key = graphene.NonNull(graphene.String)
    nickname = graphene.NonNull(graphene.String)


class GetUserInfoReturnType(graphene.ObjectType):
    #sns_profile_img = 
    sns_nickname = graphene.NonNull(graphene.String)
    account_pub_key = graphene.NonNull(graphene.String)
    account_nickname = graphene.NonNull(graphene.String)
    inbox_list = graphene.List(graphene.NonNull(InboxType))
