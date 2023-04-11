import graphene
from sns.models import SNS, SNSConnectionInfo
from blockchain.models import Wallet, Network
from genie_backend.utils import errors


class RegisterSNS(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)
        #profile_img = graphene ~~~

    def mutate(self, info, network_name, address, sns_name, handle, profile_img=None):
        network_name = network_name.strip()
        address = address.strip()
        sns_name = sns_name.strip()
        handle = handle.strip()
        
        network = Network.get_by_name(network_name)
        sns = SNS.get_by_name(sns_name)
        wallet = Wallet.get_by_network_address(network, address)
        account = wallet.account

        try:    
            SNSConnectionInfo.objects.create(account=account, sns=sns, handle=handle, profile_img=profile_img)
        except Exception:
            errors.RegisterSNSFailure

        return RegisterSNS(success=True)


class UnregisterSNS(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        address = graphene.String(required=True)
        sns_name = graphene.String(required=True)
        handle = graphene.String(required=True)

    def mutate(self, info, network_name, address, sns_name, handle):
        network_name = network_name.strip()
        address = address.strip()
        sns_name = sns_name.strip()
        handle = handle.strip()
        
        network = Network.get_by_name(network_name)
        sns = SNS.get_by_name(sns_name)
        wallet = Wallet.get_by_network_address(network, address)
        account = wallet.account
        
        sns_connection = SNSConnectionInfo.get_sns_connection(sns=sns, account=account, handle=handle)
        
        sns_connection.delete()
        
        return UnregisterSNS(success=True)


class SNSMutation(graphene.ObjectType):
    register_sns = RegisterSNS.Field()
    unregister_sns = UnregisterSNS.Field()
