from csv import DictWriter



class Database(object):

    __slots__ = ('__field_names', '__file_descriptor', '__writer', '__data')


    def __init__(self, file_location: str) -> None:
        self.__field_names = None
        self.__data = list()
        self.__file_descriptor = file_location
        # self.__file_descriptor = open(file_location, 'w')
        # self.__writer = None
        return



    def __del__(self) -> None:
        # self.__file_descriptor.close()
        return



    def write_database(self, data: dict):
        keys = tuple(data.keys())
        if self.__field_names is None:
            self.__field_names = keys
            with open(self.__file_descriptor, 'w') as f:
                f.write(f"{','.join(keys)}\n")
            # self.__writer = DictWriter(self.__file_descriptor, fieldnames=keys)
            # self.__writer.writeheader()
        assert keys == self.__field_names, 'Inconsistency in csv field names.'
        data_as_str = [self.__format_string(d) for d in data.values()]
        with open(self.__file_descriptor, 'a') as f:
            f.write(f"{','.join(data_as_str)}\n")
        return



    def __format_string(self, any) -> str:
        if any is None:
            return ''
        return str(any).replace(',', ' ')
