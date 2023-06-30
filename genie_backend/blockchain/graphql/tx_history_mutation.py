import graphene
from django.db.models import QuerySet
from accounts.models import Inbox
from sns.models import SNS, SNSConnectionInfo, Server
from blockchain.models import Network, NFT, Coin, NFTTransactionHistory, CoinTransactionHistory
from genie_backend.utils import errors


class UploadNFTTransactionHistory(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        server_name = graphene.String(required=True)
        from_discriminator = graphene.String(required=True)
        to_discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        tx_hash = graphene.String(required=True)
        nft_address = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        sns_name: str,
        server_name: str,
        from_discriminator: str,
        to_discriminator: str,
        network_name: str,
        tx_hash: str,
        nft_address: str,
    ) -> "UploadNFTTransactionHistory":
        sns = SNS.get_by_name(sns_name)
        server = Server.get_by_name(sns, server_name)
        from_account = SNSConnectionInfo.get_account(sns, from_discriminator)
        to_account = SNSConnectionInfo.get_account(sns, to_discriminator)
        network = Network.get_by_name(network_name)
        from_inbox = Inbox.get_inbox(sns, from_account, network)
        to_inbox = Inbox.get_inbox(sns, to_account, network)
        nft = NFT.get_by_address(network, nft_address)

        try:
            NFTTransactionHistory.objects.create(
                from_inbox=from_inbox, to_inbox=to_inbox, tx_hash=tx_hash, server=server, nft=nft
            )
        except Exception:
           raise errors.NFTTxHistoryFailure from Exception 

        return UploadNFTTransactionHistory(success=True)


class UploadCoinTransactionHistory(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        server_name = graphene.String(required=True)
        from_discriminator = graphene.String(required=True)
        to_discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        tx_hash = graphene.String(required=True)
        coin_address = graphene.String(required=True)
        amount = graphene.Float(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        sns_name: str,
        server_name: str,
        from_discriminator: str,
        to_discriminator: str,
        network_name: str,
        tx_hash: str,
        coin_address: str,
        amount: float,
    ) -> "UploadCoinTransactionHistory":
        sns = SNS.get_by_name(sns_name)
        server = Server.get_by_name(sns, server_name)
        from_account = SNSConnectionInfo.get_account(sns, from_discriminator)
        to_account = SNSConnectionInfo.get_account(sns, to_discriminator)
        network = Network.get_by_name(network_name)
        from_inbox = Inbox.get_inbox(sns, from_account, network)
        to_inbox = Inbox.get_inbox(sns, to_account, network)
        coin = Coin.get_by_address(network, coin_address)

        try:
            CoinTransactionHistory.objects.create(
                from_inbox=from_inbox, to_inbox=to_inbox, tx_hash=tx_hash, server=server, coin=coin, amount=amount
            )
        except Exception:
           raise errors.CoinTxHistoryFailure from Exception 

        return UploadCoinTransactionHistory(success=True)


class TxHistoryMutation(graphene.ObjectType):
    upload_coin_transaction_history = UploadCoinTransactionHistory.Field()
    upload_nft_transaction_history = UploadNFTTransactionHistory.Field()
