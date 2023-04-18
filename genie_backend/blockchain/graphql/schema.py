from blockchain.models import Wallet
from graphene_django.types import DjangoObjectType


class WalletType(DjangoObjectType):
    class Meta:
        model: "Wallet" = Wallet
