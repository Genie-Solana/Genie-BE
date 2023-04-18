from typing import Optional
import graphene
from django.db.models import QuerySet
from sns.graphql.schema import ServerType
from sns.models import Server


class ServerQuery(graphene.ObjectType):
    servers: bool = graphene.NonNull(
        graphene.List(graphene.NonNull(ServerType)), sns_name=graphene.String()
    )

    def resolve_servers(
        self, info: graphene.ResolveInfo, **kwargs
    ) -> QuerySet["Server"]:
        sns_name: Optional[str] = kwargs.get("sns_name")

        if sns_name is None:
            return Server.objects.all()
        return Server.objects.filter(sns__name=sns_name)
