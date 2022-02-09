from ext_abc import StrictMeta, abstractattribute, abstractmethod
from typing import Any
import logging
import pytest
logging.basicConfig(
    level=logging.INFO
)


class StrictClassInterface(metaclass=StrictMeta):
    @abstractattribute
    def necessary_attribute(self) -> Any: ...

    @abstractmethod
    def necessary_method(self): ...

    def optional_attribute(self) -> Any: ...

    def optional_method(self): ...


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
