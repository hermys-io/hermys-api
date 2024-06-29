from b2sdk.v2 import (  # type: ignore
    AuthInfoCache,
    B2Api,
    InMemoryAccountInfo,
    UploadSourceBytes,
)
from fastapi import UploadFile


class B2Service:
    def __init__(self) -> None:
        info = InMemoryAccountInfo()
        b2_api = B2Api(info, cache=AuthInfoCache(info))
        application_key_id = '0052bc4a3ccc98c0000000001'
        application_key = 'K005F++RHvp8RQAmp8I35LAl+cuheh0'
        b2_api.authorize_account(
            'production',
            application_key_id,
            application_key,
        )
        self.bucket = b2_api.get_bucket_by_name('hermys-dev')

    def upload_file(self, file: UploadFile) -> str:
        filename = f'folder/{file.filename}'
        upload_source = UploadSourceBytes(data_bytes=file.file.read())
        uploaded_file = self.bucket.upload(
            upload_source=upload_source, file_name=filename
        )

        return uploaded_file.file_name

    def get_file(self, filename: str) -> str:
        url = self.bucket.get_download_url(filename=filename)
        authorization = self.bucket.get_download_authorization(
            file_name_prefix=filename,
            valid_duration_in_seconds=600,
        )

        return f'{url}?Authorization={authorization}'
