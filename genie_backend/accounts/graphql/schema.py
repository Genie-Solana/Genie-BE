import graphene
from accounts.models import SocialAccount, Inbox
from blockchain.models import Network, Wallet, Coin, Collection, NFT, CoinTransactionHistory, NFTTransactionHistory
from graphene_django.types import DjangoObjectType


class NetworkType(DjangoObjectType):
    class Meta:
        model = Network
        fields = ("name",)


class InboxType(DjangoObjectType):
    class Meta:
        model = Inbox
        fields = ("pub_key", "network")


class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet
        fields = ("address", "network")


class CoinType(DjangoObjectType):
    class Meta:
        model = Coin
        fields = ("network", "ticker", "symbol")


class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
        fields = ("network", "name", "mint_address")


class NFTType(DjangoObjectType):
    class Meta:
        model = NFT
        fields = ("network", "name", "mint_address", "collection")


class CoinTransactionHistoryType(graphene.ObjectType):
    coin = graphene.NonNull(CoinType)
    is_sent = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)
    amount = graphene.NonNull(graphene.Float)
    target_sns_nickname = graphene.NonNull(graphene.String)
    target_social_nickname = graphene.NonNull(graphene.String)
    created_at = graphene.NonNull(graphene.DateTime)


class NFTTransactionHistoryType(graphene.ObjectType):
    NFT = graphene.NonNull(NFTType)
    is_sent = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)
    target_sns_nickname = graphene.NonNull(graphene.String)
    target_social_nickname = graphene.NonNull(graphene.String)
    created_at = graphene.NonNull(graphene.DateTime)


class GetUserTxHistoryReturnType(graphene.ObjectType):
    nft_tx_list = graphene.List(graphene.NonNull(NFTTransactionHistoryType))
    coin_tx_list = graphene.List(graphene.NonNull(CoinTransactionHistoryType))


class GetUserWalletAddressReturnType(graphene.ObjectType):
    wallet_list = graphene.List(graphene.NonNull(WalletType))


class GetAccountInfoReturnType(graphene.ObjectType):
    pub_key = graphene.NonNull(graphene.String)
    nickname = graphene.NonNull(graphene.String)


class GetUserInfoReturnType(graphene.ObjectType):
    #sns_profile_img = 
    sns_nickname = graphene.NonNull(graphene.String)
    account_pub_key = graphene.NonNull(graphene.String)
    account_nickname = graphene.NonNull(graphene.String)
    inbox_list = graphene.List(graphene.NonNull(InboxType))
