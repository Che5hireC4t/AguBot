class BadPasswordException(RuntimeError):

    __slots__ = ('__bad_password',)

    def __init__(self, bad_password: str, error_message: str = '') -> None:
        self.__bad_password = str(bad_password)
        super().__init__(str(error_message))


    def __get_bad_password(self) -> str:
        return self.__bad_password

    bad_password = property(fget=__get_bad_password, doc=f"{__get_bad_password.__doc__}")
