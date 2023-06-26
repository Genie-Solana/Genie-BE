import graphene
from accounts.models import SocialAccount
from graphene_django.types import DjangoObjectType


class GetAccountInfoReturnType(graphene.ObjectType):
    success = graphene.NonNull(graphene.Boolean)
    pub_key = graphene.NonNull(graphene.String)
    nickname = graphene.NonNull(graphene.String)
