from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pydantic_core import PydanticCustomError, core_schema


class ObjectIdField(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        object_id_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]
        )
        return core_schema.json_or_python_schema(
            json_schema=object_id_schema,
            python_schema=core_schema.union_schema(
                [core_schema.is_instance_schema(ObjectId), object_id_schema]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value: str):
        try:
            return ObjectId(value)
        except InvalidId as invalid_id:
            raise PydanticCustomError(
                'value_error', 'invalid format for MongoDB object identifier'
            ) from invalid_id
