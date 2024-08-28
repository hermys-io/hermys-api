from typing import Literal


def get_clerk_filename(
    *,
    organization: str,
    clerk_id: str,
    photo_name: str,
    _type: Literal['light', 'dark'],
):
    path = f'{organization}/clerk/{clerk_id}-{_type}'
    file_name = 'photo'
    file_extension = photo_name.split('.')[-1]

    return f'{path}/{file_name}.{file_extension}'


def get_knowledge_filename(
    *,
    organization: str,
    knowledge_id: str,
    photo_name: str,
):
    path = f'{organization}/knowledge/{knowledge_id}'
    file_name = 'photo'
    file_extension = photo_name.split('.')[-1]

    return f'{path}/{file_name}.{file_extension}'
