import abc


class UserInterface(metaclass=abc.ABCMeta):

    '''@abc.abstractproperty
    def id(self):
        pass

    @abc.abstractproperty
    def first_name(self) -> str:
        pass

    @abc.abstractproperty
    def last_name(self) -> str:
        pass

    @abc.abstractproperty
    def email(self) -> str:
        pass

    @abc.abstractproperty
    def password(self) -> str:
        pass

    @abc.abstractproperty
    def Permission(self) -> str:
        pass

    @abc.abstractmethod
    def verify(self, password: str) -> bool:
        pass

    @abc.abstractmethod
    def deactivate(self):
        pass'''

class UserRepositoryInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self):
        pass

 