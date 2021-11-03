from typing import Any, Final

import boto3
from boto3.dynamodb.conditions import Attr


class DynamoDbDict:
    # noinspection PyMissingConstructor
    def __init__(self, table_name: str, hash_key_name: str = "id") -> None:
        self.__table_name: Final[str] = table_name
        self.__hash_key_name: Final[str] = hash_key_name
        self.__table_resource = boto3.resource("dynamodb").Table(table_name)

    def set_if_not_present(self, name: str, value: Any) -> None:
        self.set(name, value, no_overwrites=True)

    def set(self, name: str, value: Any, no_overwrites: bool = False) -> None:
        db_item = {self.__hash_key_name: name,
                   "Value": value}

        put_item_request = {"Item": db_item}

        if no_overwrites:
            put_item_request['ConditionExpression'] = Attr(self.__hash_key_name).not_exists()

        self.__table_resource.put_item(**put_item_request)

    def get(self, name: str, consistent_read: bool = True) -> Any:
        get_item_result = self.__table_resource.get_item(Key={self.__hash_key_name: name}, ConsistentRead=consistent_read)

        if 'Item' in get_item_result and len(get_item_result.keys()) > 0:
            return get_item_result['Item']['Value']

        raise KeyError(f"{name} does not exist in DDB Table \"{self.__table_name}\"")

    def delete(self, name: str) -> None:
        self.__table_resource.delete_item(Key={self.__hash_key_name: name})
