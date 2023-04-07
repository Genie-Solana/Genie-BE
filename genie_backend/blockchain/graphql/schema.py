from blockchain.models import Wallet
import graphene
from graphene_django.types import DjangoObjectType


class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet
