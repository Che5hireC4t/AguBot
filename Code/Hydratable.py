from re import compile, sub


class Hydratable(object):

    __CAMEL_CASE_REGEXP = compile(r'(?<!^)(?=[A-Z])')


    def __init__(self, **kwargs) -> None:
        return


    @classmethod
    def hydrate(cls, data: dict):
        snake_case_arguments = {cls.__to_snake_case(key): value for key, value in data.items()}
        return cls(**snake_case_arguments)


    @classmethod
    def __to_snake_case(cls, camel_case_string: str) -> str:
        string = sub(cls.__CAMEL_CASE_REGEXP, '_', camel_case_string).lower()
        while '__' in string:
            string = string.replace('__', '_')
        string = string.replace('_u_t_c', '_utc')
        return string
