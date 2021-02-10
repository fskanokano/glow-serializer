from collections import OrderedDict
from typing import Union, List

from .meta import SerializerMeta


class Serializer(object, metaclass=SerializerMeta):

    def __init__(self, *, exclude: list = None, many: bool = False):
        if exclude is None:
            exclude = []
        self.exclude = exclude
        self.many = many

    def __get_nested_value(self, field, value):
        field = getattr(self, field, None)
        serializer = getattr(field, 'serializer', None)
        if serializer is None:
            value = None
        elif isinstance(serializer, Serializer):
            value = serializer.dumps(value, many=serializer.many)
        else:
            value = None
        return value

    def __iterate_fields(self, obj, fields, nested_fields):
        data = OrderedDict()
        for field in fields:
            value = getattr(obj, field, None)
            if field not in nested_fields:
                data[field] = value
            else:
                value = self.__get_nested_value(field, value)
                data[field] = value
        return data

    def dumps(self, obj, *, many: bool = False) -> Union[OrderedDict, List[OrderedDict]]:
        fields = self.fields
        if self.exclude:
            fields = [field for field in fields if field not in self.exclude]
        nested_fields = self.nested_fields
        if not many:
            data = self.__iterate_fields(obj, fields, nested_fields)
            return data
        else:
            data_list = []
            for _obj in obj:
                data = self.__iterate_fields(_obj, fields, nested_fields)
                data_list.append(data)
            return data_list
