from .models import User
from .repositories import UserRepositoryInterface
from .exceptions import PixyProxyException, RecordNotFoundError
from .db_context import DatabaseContext, get_current_db_context
import traceback


class UserServiceInterface:
    def authenticate_user(self, username: str) -> User:
        pass


class UserService(UserServiceInterface):
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def authenticate_user(self, username: str) -> User:
        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                user = self.user_repo.authenticate_user(username)
                db.commit_transaction()
                if user is None:
                    raise RecordNotFoundError()
                return user
            except PixyProxyException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise PixyProxyException("An unexpected error occurred while processing your request.") from e
