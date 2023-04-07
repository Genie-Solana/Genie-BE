from graphene_django.views import GraphQLView as BaseGraphQLView


class GraphQLView(BaseGraphQLView):
    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)

        try:
            formatted_error["context"] = error.original_error.context
        except AttributeError:
            pass

        return formatted_error


class GenieGraphQLException(Exception):
    message = None
    error_msg = None

    def __init__(
        self,
    ):
        self.context = {}

        if self.error_msg:
            self.context["error_msg"] = self.error_msg

        super().__init__(self.message)


class UserNotFound(GenieGraphQLException):
    # Exception Example
    # TODO : Change after defining real Error case

    error_code = "A00001"
    message = "Does Not Exist!!!"
    error_msg = "There isn't user given information."


class SNSNotFound(GenieGraphQLException):
    error_code = "A00002"
    message = "Does Not Exist!!!"
    error_msg = "SNS does not exist. Please check again."


class ServerNotFound(GenieGraphQLException):
    error_code = "A00003"
    message = "Does Not Exist!!!"
    error_msg = "Server does not exist. Please check again."


class CreateServerFailure(GenieGraphQLException):
    error_code = "A00004"
    message = "Working Failure!!!"
    error_msg = "Failed to create server."


class WalletNotFound(GenieGraphQLException):
    error_code = "A00005"
    message = "Does Not Exist!!!"
    error_msg = "Wallet does not exist. Please check again."


class RegisterSNSFailure(GenieGraphQLException):
    error_code = "A00006"
    message = "Working Failure!!!"
    error_msg = "Failed to register SNS."


class NetworkNotFound(GenieGraphQLException):
    error_code = "A00007"
    message = "Does Not Exist!!!"
    error_msg = "Network does not exist. Please check again."


class SNSConnectionNotFound(GenieGraphQLException):
    error_code = "A00008"
    message = "Does Not Exist!!!"
    error_msg = "SNS Connection does not exist. Please check again."
