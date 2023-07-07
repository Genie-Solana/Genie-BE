from typing import Optional
import graphene
from django.conf import settings
from django.db.models import QuerySet
from accounts.models import Inbox
from accounts.graphql.schema import InboxType, GetAccountInfoReturnType, GetUserInfoReturnType, GetUserWalletAddressReturnType, NFTTransactionHistoryType, CoinTransactionHistoryType, GetUserTxHistoryReturnType
from blockchain.models import Wallet, Network, CoinTransactionHistory, NFTTransactionHistory
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

    get_user_tx_history = graphene.NonNull(
        GetUserTxHistoryReturnType,
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

        try:
            sns_profile_img = sns_connection_info.profile_img.url
        except:
            sns_profile_img = ""
        
        sns_nickname = sns_connection_info.handle
        account_pub_key = social_account.pub_key
        account_nickname = social_account.nickname
        try:
            account_profile_img = social_account.profile_img.url
        except:
            account_profile_img = ""
        inbox_list = Inbox.objects.filter(account=social_account)

        return GetUserInfoReturnType(
            sns_profile_img=sns_profile_img,
            sns_nickname=sns_nickname,
            account_pub_key=account_pub_key,
            account_nickname=account_nickname,
            account_profile_img=account_profile_img,
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
        
    def resolve_get_user_tx_history(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")

        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)
        inbox_list = Inbox.objects.filter(account=social_account)
        nft_tx_list = []
        coin_tx_list = []

        for inbox in inbox_list:
            for tx in NFTTransactionHistory.objects.filter(from_inbox=inbox):
                to_account = tx.to_inbox.account
                to_sns_nickname = SNSConnectionInfo.objects.get(sns=tx.to_inbox.sns, account=to_account).handle
                nft_tx_list.append(
                    NFTTransactionHistoryType(
                        NFT=tx.nft,
                        is_sent=True,
                        tx_hash=tx.tx_hash,
                        target_sns_nickname=to_sns_nickname,
                        target_social_nickname=to_account.nickname,
                        created_at=tx.created_at,
                    )
                )
            for tx in NFTTransactionHistory.objects.filter(to_inbox=inbox):
                from_account = tx.from_inbox.account
                from_sns_nickname = SNSConnectionInfo.objects.get(sns=tx.from_inbox.sns, account=from_account).handle
                nft_tx_list.append(
                    NFTTransactionHistoryType(
                        NFT=tx.nft,
                        is_sent=False,
                        tx_hash=tx.tx_hash,
                        target_sns_nickname=from_sns_nickname,
                        target_social_nickname=from_account.nickname,
                        created_at=tx.created_at,
                    )
                )
            for tx in CoinTransactionHistory.objects.filter(from_inbox=inbox):
                to_account = tx.to_inbox.account
                to_sns_nickname = SNSConnectionInfo.objects.get(sns=tx.to_inbox.sns, account=to_account).handle
                coin_tx_list.append(
                    CoinTransactionHistoryType(
                        coin=tx.coin,
                        is_sent=True,
                        tx_hash=tx.tx_hash,
                        amount=str(tx.amount),
                        target_sns_nickname=to_sns_nickname,
                        target_social_nickname=to_account.nickname,
                        created_at=tx.created_at,
                    )
                )
            for tx in CoinTransactionHistory.objects.filter(to_inbox=inbox):
                from_account = tx.from_inbox.account
                from_sns_nickname = SNSConnectionInfo.objects.get(sns=tx.from_inbox.sns, account=from_account).handle
                coin_tx_list.append(
                    CoinTransactionHistoryType(
                        coin=tx.coin,
                        is_sent=False,
                        tx_hash=tx.tx_hash,
                        amount=str(tx.amount),
                        target_sns_nickname=from_sns_nickname,
                        target_social_nickname=from_account.nickname,
                        created_at=tx.created_at,
                    )
                )

        return GetUserTxHistoryReturnType(
            nft_tx_list=nft_tx_list,
            coin_tx_list=coin_tx_list,
        )

