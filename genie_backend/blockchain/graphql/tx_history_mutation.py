import graphene
import requests
from django.db.models import QuerySet
from django.core.files.base import ContentFile
from accounts.models import Inbox
from sns.models import SNS, SNSConnectionInfo, Server
from blockchain.models import Network, NFT, Coin, NFTTransactionHistory, CoinTransactionHistory, Collection
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
        nft_name = graphene.String(required=True)
        nft_image_url = graphene.String(required=True)
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
        nft_name: str,
        nft_image_url: str,
        nft_address: str,
    ) -> "UploadNFTTransactionHistory":
        sns = SNS.get_by_name(sns_name)
        server = Server.get_by_name(sns, server_name)
        from_account = SNSConnectionInfo.get_account(sns, from_discriminator)
        to_account = SNSConnectionInfo.get_account(sns, to_discriminator)
        network = Network.get_by_name(network_name)
        from_inbox = Inbox.get_inbox(sns, from_account, network)
        to_inbox = Inbox.get_inbox(sns, to_account, network)
        
        try:
            nft = NFT.get_by_address(network, nft_address)
            if not nft.image:
                try:
                    response = requests.get(nft_image_url)
                    image_content = response.content
                    image = ContentFile(image_content, f'{nft_address}.png')
                except:
                    image = None
                nft.image = image
                nft.save()
        except:
            try:
                response = requests.get(nft_image_url)
                image_content = response.content
                image = ContentFile(image_content, f'{nft_address}.png')
            except:
                image = None

            collection = Collection.objects.get(network=network, name="NOT REGISTERED COLLECTION")
            nft = NFT.objects.create(
                network=network, name=nft_name, mint_address=nft_address, collection=collection, image=image
            )

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
        coin_name = graphene.String(required=True)
        coin_ticker = graphene.String(required=True)
        coin_symbol_url = graphene.String(required=True)
        coin_address = graphene.String(required=True)
        amount = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        sns_name: str,
        server_name: str,
        from_discriminator: str,
        to_discriminator: str,
        network_name: str,
        tx_hash: str,
        coin_name: str,
        coin_ticker: str,
        coin_symbol_url: str,
        coin_address: str,
        amount: str,
    ) -> "UploadCoinTransactionHistory":
        sns = SNS.get_by_name(sns_name)
        server = Server.get_by_name(sns, server_name)
        from_account = SNSConnectionInfo.get_account(sns, from_discriminator)
        to_account = SNSConnectionInfo.get_account(sns, to_discriminator)
        network = Network.get_by_name(network_name)
        from_inbox = Inbox.get_inbox(sns, from_account, network)
        to_inbox = Inbox.get_inbox(sns, to_account, network)
    
        try:
            coin = Coin.get_by_address(network, coin_address)
            if not coin.symbol:
                try:
                    response = requests.get(coin_symbol_url)
                    image_content = response.content
                    image = ContentFile(image_content, f'{coin_address}.png')
                except:
                    image = None
                coin.symbol = image
                coin.save()
        except:
            try:
                response = requests.get(coin_symbol_url)
                image_content = response.content
                image = ContentFile(image_content, f'{coin_address}.png')
            except:
                image = None

            coin = Coin.objects.create(
                network=network, name=coin_name, mint_address=coin_address, ticker=coin_ticker, symbol=image
            )


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
