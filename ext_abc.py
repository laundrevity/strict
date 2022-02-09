# Conor L. Mahany, 2022-02-09
from typing import Callable
import logging
logging.basicConfig(
    level=logging.INFO
)


class DummyAttribute:
    pass


class DummyMethod:
    def __call__(self):
        return None


def abstractattribute(obj=None):
    if obj is None:
        obj = DummyAttribute()
    obj.__is_abstract_attribute__ = True
    return obj


def abstractmethod(obj=None):
    if obj is None:
        obj = DummyMethod()
    obj.__is_abstract_method__ = True
    return obj


class StrictMeta(type):
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls, name, bases, namespace, **kwargs):
        return super().__init__(name, bases, namespace, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        abstract_attributes = {
            key for key in dir(instance)
            if not key.startswith('__')
            and getattr(
                getattr(instance, key),
                '__is_abstract_attribute__',
                False
            )
        }
        if abstract_attributes:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"without attributes {', '.join(abstract_attributes)}"
                )
            )

        abstract_methods = {
            key for key in dir(instance)
            # if isinstance(getattr(instance, key), Callable)
            if not key.startswith('__')
            and getattr(getattr(instance, key), '__is_abstract_method__', False)
        }
        if abstract_methods:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"without methods {', '.join(abstract_methods)}"
                )
            )

        logging.info(f"{cls.__bases__=}")
        parent = cls.__bases__[0]
        invalid_methods = {
            key for key in dir(instance)
            if not isinstance(getattr(instance, key), Callable)
            and not key.startswith('__')
            and getattr(getattr(parent, key), '__is_abstract_method__', False)
        }
        if invalid_methods:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"with non-callable methods {' ,'.join(invalid_methods)}"
                )
            )

        return instance
