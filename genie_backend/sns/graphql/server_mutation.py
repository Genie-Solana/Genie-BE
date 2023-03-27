import graphene
from sns.graphql.schema import ServerType
from sns.models import Server, SNS
from genie_backend.utils import errors


class CreateServer(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        server_name = graphene.String(required=True)
        sns_name = graphene.String(required=True)

    def mutate(self, info, server_name, sns_name):
        server_name = server_name.strip()
        sns = SNS.get_by_name(sns_name)

        try:
            server = Server(name=server_name, sns=sns)
            server.save()
        except Exception as e:
            print(e)

        return CreateServer(success=True)


class EditServer(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    server = graphene.Field(graphene.NonNull(ServerType))

    class Arguments:
        server_id = graphene.Int(required=True)
        update_server_name = graphene.String()
        update_sns_name = graphene.String()

    def mutate(self, info, server_id, update_server_name=None, update_sns_name=None):
        server = Server.get_server(server_id)
        
        if update_server_name is not None:
            server.name = update_server_name
        if update_sns_name is not None:
            server.sns = SNS.get_by_name(update_sns_name)

        server.save()

        return EditServer(success=True, server=server)


class DeleteServer(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        server_id = graphene.Int(required=True)

    def mutate(self, info, server_id):
        server = Server.get_server(server_id)

        server.delete()

        return DeleteServer(success=True)


class ServerMutation(graphene.ObjectType):
    create_server = CreateServer.Field()
    edit_server = EditServer.Field()
    delete_server = DeleteServer.Field()
