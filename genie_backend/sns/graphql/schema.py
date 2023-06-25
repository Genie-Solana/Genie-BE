from sns.models import Server, SNS
from graphene_django.types import DjangoObjectType


class ServerType(DjangoObjectType):
    class Meta:
        model: "Server" = Server


class SNSType(DjangoObjectType):
    class Meta:
        model: "SNS" = SNS
