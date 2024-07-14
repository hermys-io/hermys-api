def get_clerk_filename(*, organization: str, clerk_id: str, photo_name: str):
    path = f'{organization}/clerk/{clerk_id}'
    file_name = 'photo'
    file_extension = photo_name.split('.')[-1]

    return f'{path}/{file_name}.{file_extension}'
