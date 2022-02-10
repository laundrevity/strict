# Conor L. Mahany, 2022-02-09
from ext_abc import StrictMeta, abstract_attribute, abstract_method, final_attribute, final_method
from typing import Any
import logging
import pytest
logging.basicConfig(
    level=logging.INFO
)


class StrictClassInterface(metaclass=StrictMeta):
    @abstract_attribute
    def necessary_attribute(self) -> Any: ...

    @abstract_method
    def necessary_method(self): ...

    def optional_attribute(self) -> Any: ...

    def optional_method(self): ...

    @final_attribute
    def illegal_attribute(self) -> Any:
        return "you mustn't change this..."

    @final_method
    def illegal_method(self, x: float):
        return x*x+1


class MissingAttribute(StrictClassInterface):
    def necessary_method(self):
        pass


class MissingMethod(StrictClassInterface):
    necessary_attribute = None


class InvalidMethod(StrictClassInterface):
    necessary_attribute = None
    necessary_method = None


class MinimalStrictClass(StrictClassInterface):
    necessary_attribute = None
    # necessary_method = None  # this shouldn't work...

    def necessary_method(self):
        return None


class MaximalStrictClass(StrictClassInterface):
    def __init__(self):
        self.necessary_attribute = None
        self.optional_attribute = None

    def necessary_method(self):
        pass

    def optional_method(self):
        pass


class BadClassA(StrictClassInterface):
    necessary_attribute = None
    illegal_attribute = 'orly??'

    def necessary_method(self):
        return None


class BadClassB(StrictClassInterface):
    necessary_attribute = None

    def necessary_method(self):
        return None

    def illegal_method(self):
        return 'whatcha gonna do about it??'


def test_main():
    try:
        _ = MissingAttribute()
        a = 1/0
    except NotImplementedError as e:
        logging.info(e)

    try:
        _ = MissingMethod()
        a = 1/0
    except NotImplementedError as e:
        logging.info(e)

    try:
        _ = InvalidMethod()
        a = 1/0
    except NotImplementedError as e:
        logging.info(e)

    assert MinimalStrictClass()
    assert MaximalStrictClass()


def test_final():
    try:
        bc = BadClassA()
        a = 1/0
    except NotImplementedError as e:
        logging.info(e)

    try:
        BadClassB()
    except NotImplementedError as e:
        logging.info(e)
