from typing import Type

from .field import NestedField


class SerializerMeta(type):

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        meta = attrs.get('Meta', None)
        fields = mcs.__search_fields(meta)
        nested_fields = mcs.__search_nested_fields(attrs)
        attrs['fields'] = fields
        attrs['nested_fields'] = nested_fields
        return super().__new__(mcs, name, bases, attrs)

    @staticmethod
    def __search_fields(meta: Type[object]):
        fields = getattr(meta, 'fields', [])
        return fields

    @staticmethod
    def __search_nested_fields(attrs: dict):
        return [key for key, value in attrs.items() if isinstance(value, NestedField)]
