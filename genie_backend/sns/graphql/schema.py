from sns.models import Server, SNS
import graphene
from graphene_django.types import DjangoObjectType


class ServerType(DjangoObjectType):
    class Meta:
        model = Server


class SNSType(DjangoObjectType):
    class Meta:
        model = SNS

