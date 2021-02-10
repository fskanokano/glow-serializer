from collections import OrderedDict
from typing import Union, List

from .meta import SerializerMeta


class Serializer(object, metaclass=SerializerMeta):

    def __init__(self, *, exclude: list = None, many: bool = False):
        """
        初始化序列器
        :param exclude:需要排除的字段
        :param many: 是否为多条数据，用于反向查询的外键字段中
        """
        if exclude is None:
            exclude = []
        self.exclude = exclude
        self.many = many

    def __get_nested_value(self, field, value):
        """
        对外键字段进行序列化
        :param field: 外键字段名称
        :param value: 外键对象
        :return: 序列化的值
        """
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
        """
        遍历需要序列化的字段
        :param obj: 需要序列化的对象
        :param fields: 需要序列化的字段
        :param nested_fields: 外键字段
        :return:
        """
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
        """
        序列化orm对象
        :param obj:需要序列化的对象
        :param many: 该对象是否有多条
        :return: 序列化后的数据
        """
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
