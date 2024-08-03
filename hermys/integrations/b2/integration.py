from b2sdk.v2 import (  # type: ignore
    AuthInfoCache,
    B2Api,
    InMemoryAccountInfo,
    UploadSourceBytes,
)
from fastapi import UploadFile

from hermys.settings import get_settings

settings = get_settings()


class B2Integration:
    def __init__(self) -> None:
        info = InMemoryAccountInfo()
        b2_api = B2Api(info, cache=AuthInfoCache(info))
        application_key_id = settings.B2_APPLICATION_KEY_ID
        application_key = settings.B2_APPLICATION_KEY
        b2_api.authorize_account(
            'production',
            application_key_id,
            application_key,
        )
        self.bucket = b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

    def upload_file(self, file: UploadFile, file_name: str) -> str:
        upload_source = UploadSourceBytes(data_bytes=file.file.read())
        uploaded_file = self.bucket.upload(
            upload_source=upload_source, file_name=file_name
        )

        return uploaded_file.file_name

    def get_file(self, filename: str, valid_duration_in_seconds: int) -> str:
        url = self.bucket.get_download_url(filename=filename)
        authorization = self.bucket.get_download_authorization(
            file_name_prefix=filename,
            valid_duration_in_seconds=valid_duration_in_seconds,
        )

        return f'{url}?Authorization={authorization}'
