from typing import Type, Optional
import graphene
from sns.graphql.schema import ServerType
from sns.models import Server, SNS
from genie_backend.utils import errors


class CreateServer(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        server_name = graphene.String(required=True)
        sns_name = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        server_name: str,
        sns_name: str,
    ) -> graphene.Mutation:
        _server_name: str = server_name.strip()
        _sns_name: str = sns_name.strip()
        sns: SNS = SNS.get_by_name(_sns_name)

        try:
            Server.objects.create(name=_server_name, sns=sns)
        except Exception:
            raise errors.CreateServerFailure from Exception

        return CreateServer(success=True)


class EditServer(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)
    server: Type["ServerType"] = graphene.Field(graphene.NonNull(ServerType))

    class Arguments:
        server_id = graphene.Int(required=True)
        update_server_name = graphene.String()
        update_sns_name = graphene.String()

    def mutate(
        self,
        info: graphene.ResolveInfo,
        server_id: int,
        update_server_name: Optional[str] = None,
        update_sns_name: Optional[str] = None,
    ) -> graphene.Mutation:
        server: "Server" = Server.get_server(server_id)

        if update_server_name is not None:
            server.name = update_server_name
        if update_sns_name is not None:
            server.sns = SNS.get_by_name(update_sns_name)

        server.save()

        return EditServer(success=True, server=server)


class DeleteServer(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        server_id = graphene.Int(required=True)

    def mutate(self, info: graphene.ResolveInfo, server_id: int) -> graphene.Mutation:
        server: "Server" = Server.get_server(server_id)

        server.delete()

        return DeleteServer(success=True)


class ServerMutation(graphene.ObjectType):
    create_server = CreateServer.Field()
    edit_server = EditServer.Field()
    delete_server = DeleteServer.Field()
