from repository.interface import UserRepositoryInterface
from entities.user import User

class UserRepository(UserRepositoryInterface):
    def __init__():
        pass

    def find(self, name: str) -> User:
        user = self._find_user_account({'username': name})
        return self._factory_credential(user)

    def find_by(self, name: str) -> User:
        user = self._find_user_account({'username': name})
        return self._fa
        ctory_credential(user)

    def create(self, user: User) -> User:
        user = User(
            name=user.name,
            email=user.email,
            password=user.password,
        )
        user.save()
        return self._factory_credential(user)

    def update_email(self, email: str) -> User:
        user = self._find_user_account({'uuid': credential.uuid})
        user.is_active = credential.active
        user.save()

        return self._factory_credential(user)

    def update_password(self, credential: CredentialInterface) -> Credential:
        user = self._find_user_account({'uuid': credential.uuid})
        user.password = credential.password.value
        user.save()

        return self._factory_credential(user)

    def _factory_credential(self, user: UserAccount) -> Credential:
        if user:
            return Credential(
                user.username,
                user.password,
                uuid=user.uuid,
                active=user.is_active
            )

    def _find_user_account(self, params: dict) -> UserAccount:
        try:
            user = UserAccount.objects.get(**params)
        except ObjectDoesNotExist:
            return None
        else:
            return user
