import pytest
from bson import ObjectId
from pydantic_core import PydanticCustomError

from hermys.db.base import ObjectIdField


@pytest.mark.anyio
async def test_object_id_field_validate():
    result = ObjectIdField.validate('66ce746ef5cdb5864827e27b')
    assert result == ObjectId('66ce746ef5cdb5864827e27b')


@pytest.mark.anyio
async def test_object_id_field_validate_error():
    with pytest.raises(PydanticCustomError):
        ObjectIdField.validate('teste')
