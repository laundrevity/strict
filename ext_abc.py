# Conor L. Mahany, 2022-02-09
from typing import Callable
import logging
logging.basicConfig(
    level=logging.INFO
)


class FinalAttributeException(Exception):
    pass


class DummyAttribute:
    pass


class DummyMethod:
    def __call__(self):
        return None


def abstract_attribute(obj=None):
    if obj is None:
        obj = DummyAttribute()
    obj.__is_abstract_attribute__ = True
    return obj


def abstract_method(obj=None):
    if obj is None:
        obj = DummyMethod()
    obj.__is_abstract_method__ = True
    return obj


def final_attribute(obj=None):
    if obj is None:
        obj = DummyAttribute()
    obj.__is_final_attribute__ = True
    return obj


def final_method(obj=None):
    if obj is None:
        obj = DummyMethod()
    obj.__is_final_method__ = True
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
        keys = [key for key in dir(instance) if not key.startswith('__')]

        abstract_attributes = {
            key for key in keys
            if getattr(
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
            key for key in keys
            if getattr(
                getattr(instance, key),
                '__is_abstract_method__',
                False
            )
        }
        if abstract_methods:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"without methods {', '.join(abstract_methods)}"
                )
            )

        # logging.info(f"{cls.__bases__=}")
        parent = cls.__bases__[0]
        invalid_methods = {
            key for key in keys
            if not isinstance(getattr(instance, key), Callable)
            and getattr(getattr(parent, key), '__is_abstract_method__', False)
        }
        if invalid_methods:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"with non-callable methods {', '.join(invalid_methods)}"
                )
            )

        # logging.info(f"{cls.__name__=}")
        # for key in keys:
        #     logging.info((
        #         f"getattr(instance, {key}) = {getattr(instance, key)}"
        #     ))

        final_attributes = {
            key for key in keys
            if getattr(getattr(parent, key), '__is_final_attribute__', False)
            and not getattr(getattr(instance, key), '__is_final_attribute__', False)
        }
        if final_attributes:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"with final attributes {', '.join(final_attributes)}"
                )
            )

        final_methods = {
            key for key in keys
            if getattr(getattr(parent, key), '__is_final_method__', False)
            and not getattr(getattr(instance, key), '__is_final_method__', False)
        }
        if final_methods:
            raise NotImplementedError(
                (
                    f"Cannot instantiate abstract class {cls.__name__} "
                    f"with final methods {', '.join(final_methods)}"
                )
            )

        return instance
