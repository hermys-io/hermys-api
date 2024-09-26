import pytest

from hermys.common.b2_helpers import get_clerk_filename, get_knowledge_filename


@pytest.mark.anyio
async def test_get_clerk_filename():
    result = get_clerk_filename(
        organization='hermys',
        clerk_id='clerk_id',
        photo_name='my_photo.png',
        _type='light',
    )

    assert result == 'hermys/clerk/clerk_id-light/photo.png'


@pytest.mark.anyio
async def test_get_knowledge_filename():
    result = get_knowledge_filename(
        organization='hermys',
        knowledge_id='knowledge_id',
        photo_name='my_photo.png',
    )

    assert result == 'hermys/knowledge/knowledge_id/photo.png'
