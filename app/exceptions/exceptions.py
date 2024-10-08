class FidoTransactionAPIError(Exception):
    """base exception class"""

    def __init__(
        self, message: str = "Service is unavailable, please try again later", name: str = "FidoTransactionsAPI"
    ):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(FidoTransactionAPIError):
    """failures in external services or APIs, like a database or a third-party service"""

    pass


class EntityDoesNotExistError(FidoTransactionAPIError):
    """database returns nothing"""

    pass


class EntityAlreadyExistsError(FidoTransactionAPIError):
    """conflict detected, like trying to create a resource that already exists"""

    pass


class InvalidOperationError(FidoTransactionAPIError):
    """invalid operations like trying to delete a non-existing entity, etc."""

    pass
