import os
import random
from abc import ABC, abstractmethod
from typing import List, Final, Dict
from uuid import uuid4

from dynamodb_dict import DynamoDbDict

SLUG_LENGTH: Final[int] = 8


class AbstractShortener(ABC):
    @abstractmethod
    def shorten(self, long_url: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def expand(self, short_url: str) -> str:
        raise NotImplementedError


class Shortener0(AbstractShortener):
    """
    Basic shortener that uses UUIDs to generate the slugs.
    """
    def __init__(self) -> None:
        self.__map: Dict[str, str] = {}

    def shorten(self, long_url: str) -> str:
        while True:
            slug = str(uuid4()).replace('-', '')[:SLUG_LENGTH]

            if slug not in self.__map:
                break

        self.__map[slug] = long_url
        return slug

    def expand(self, short_url: str) -> str:
        return self.__map[short_url]


ALPHABET: Final[List[str]] = list("cdefhjkmnprtvwxy2345689")


class Shortener1(AbstractShortener):
    """
    Shortener that uses a custom alphabet to generate more human-friendly URLs
    """
    def __init__(self) -> None:
        self.__map: Dict[str, str] = {}

    def shorten(self, long_url: str) -> str:
        while True:
            slug = "".join([random.choice(ALPHABET) for i in range(SLUG_LENGTH)])

            if slug not in self.__map:
                break

        self.__map[slug] = long_url
        return slug

    def expand(self, short_url: str) -> str:
        return self.__map[short_url]


class Shortener2(AbstractShortener):
    def __init__(self) -> None:
        self.__map: DynamoDbDict = DynamoDbDict(os.getenv("TABLE_NAME"))

    def shorten(self, long_url: str) -> str:
        while True:
            slug = "".join([random.choice(ALPHABET) for i in range(SLUG_LENGTH)])

            try:
                self.__map.set_if_not_present(slug, long_url)
                break
            except Exception:
                pass

        return slug

    def expand(self, short_url: str) -> str:
        return self.__map.get(short_url)
