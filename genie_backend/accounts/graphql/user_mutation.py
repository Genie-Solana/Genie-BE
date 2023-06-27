import graphene
from accounts.models import SocialAccount
from genie_backend.utils.api_calls import create_social_account_call
from genie_backend.utils import errors


class CreateSocialAccount(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)

    class Arguments:
        nickname = graphene.String(required=True)

    def mutate(self, info, nickname):
        nickname = nickname.strip()
        try:
            data, sec_key = create_social_account_call()
            if data['success']:
                pub_key = data['data']['social_account_key']
                SocialAccount.objects.create(
                    nickname=nickname,
                    pub_key=pub_key,
                    secret_key=sec_key,
                )
                return CreateSocialAccount(success=True)
            else:
                raise errors.CreateSocialAccountFailure()
        except:
            raise errors.CreateSocialAccountFailure()


class AccountMutation(graphene.ObjectType):
    create_social_account = CreateSocialAccount.Field()
