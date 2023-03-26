import graphene
from sns.graphql.schema import ServerType
from sns.models import Server


class ServerQuery(graphene.ObjectType):
    servers = graphene.NonNull(graphene.List(graphene.NonNull(ServerType)),
        sns_name=graphene.String()
    )

    def resolve_servers(self, info, **kwargs):
        sns_name = kwargs.get("sns_name")

        if sns_name is None:
            return Server.objects.all()
        return Server.objects.filter(sns__name=sns_name)
