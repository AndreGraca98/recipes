from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import BinaryIO

from minio import Minio
from minio.error import InvalidResponseError, S3Error
from minio.helpers import ObjectWriteResult

from .env import Environment
from .logger import getLogger
from .paths import tmp_path

_log = getLogger(__name__)


class FileType(StrEnum):
    UNKNOWN = "application/octet-stream"
    PDF = "application/pdf"
    CSV = "application/csv"
    JSON = "application/json"
    GZ = "application/gzip"
    JPEG = "application/jpeg"

    def __get__(self, *_) -> str:
        """to be able to use `FileType.PDF` and get "application/pdf" """
        return self.name


class FileStore:
    """
    ```python
    from pathlib import Path
    from src.utils.filestore import FileStore, FileType

    file = Path.home() / "Pictures/broken-image.png"
    obj_name = file.stem

    store=FileStore()
    print(store.object_exists(obj_name))
    print(store.add_object(obj_name, file, FileType.JPEG))
    print(store.get_object(obj_name, Path(file.name)))
    print(store.remove_object(obj_name))
    print(store.list_objects())
    print(store.clean_up())
    """

    def __init__(self):
        self._env = Environment()

        self.bucket: str = self._env.FILESTORE_BUCKET
        self.region: str = self._env.FILESTORE_REGION
        self.should_create_bucket: bool = self._env.FILESTORE_SHOULD_CREATE_BUCKET

        self.client = Minio(
            self._env.FILESTORE_ADDRESS,
            self._env.FILESTORE_ACCESS_KEY,
            self._env.FILESTORE_SECRET_KEY,
            region=self.region,
            secure=self._env.FILESTORE_USE_HTTPS,
        )

        self.downloaded_docs: list[Path] = []

    def add_object(
        self, object_name: str, file_path: Path, file_type: str = FileType.UNKNOWN
    ):
        if not self.client.bucket_exists(self.bucket):
            if not self.should_create_bucket:
                raise BucketDoesNotExistError(self.bucket)

            try:
                self.client.make_bucket(bucket_name=self.bucket, location=self.region)
            except S3Error as err:
                # The bucket didn't exist but some other thread already created it
                code = "BucketAlreadyOwnedByYou"
                message = (
                    "Your previous request to create the named "
                    "bucket succeeded and you already own it."
                )
                if (code != err.code) or (message != err.message):
                    raise  # re-raise error

        result: ObjectWriteResult = self.client.fput_object(
            bucket_name=self.bucket,
            object_name=object_name,
            file_path=str(file_path.resolve()),
            content_type=file_type,
        )
        # sanity check
        assert result.object_name == object_name

    def remove_object(self, object_name: str):
        self.client.remove_object(bucket_name=self.bucket, object_name=object_name)

    def get_object(
        self,
        object_name: str,
        file_path: Path | None = None,
        minimum_file_size: int = 0,
    ):
        """Download object to `file_path`. if not provided will
        download to a temporary file"""
        if file_path is None:  # provide our own
            file_path = tmp_path()
        self.downloaded_docs.append(file_path)  # and keep track

        _log.debug(f"Downloading {object_name!r} from filestore")
        try:
            self.client.fget_object(
                bucket_name=self.bucket,
                object_name=object_name,
                file_path=str(file_path),
            )
        except InvalidResponseError as err:
            raise FileStoreError(f"failed downloading {object_name!r}") from err

        # at least x bytes
        if (filesize := file_path.stat().st_size) < minimum_file_size:
            raise CorruptFileError(filesize, minimum_file_size)
        return file_path

    def object_exists(self, object_name: str) -> bool:
        try:
            self.client.stat_object(bucket_name=self.bucket, object_name=object_name)
            return True
        except S3Error as err:
            if (err.code != "NoSuchKey") or (err.message != "Object does not exist"):
                raise  # re-raise error
            return False

    def list_objects(self, dir: str = ""):
        return self.client.list_objects(bucket_name=self.bucket, prefix=dir)

    def clean_up(self):
        """delete downloaded files"""
        for file in self.downloaded_docs:
            file.unlink(missing_ok=True)


def upload_to_filestore(file: BinaryIO, obj_name: str, filetype: str):
    # need to store the file temporarily
    p = tmp_path()
    p.write_bytes(file.read())

    filestore = FileStore()
    filestore.add_object(obj_name, p, filetype)

    # rm the tmp file
    p.unlink(missing_ok=True)


# context managers
class download_object:
    """context manager for downloading an object from a filestore"""

    def __init__(self, object_name: str):
        self._filestore = FileStore()
        self.object_name = object_name

    def __enter__(self) -> Path:
        return self._filestore.get_object(object_name=self.object_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._filestore.clean_up()


class download_objects:
    """context manager for downloading objects from a filestore"""

    def __init__(self, object_names: list[str]):
        self._filestore = FileStore()
        self.object_names = object_names

    def __enter__(self) -> list[Path]:
        return [self._filestore.get_object(name) for name in self.object_names]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._filestore.clean_up()


# exceptions
class FileStoreError(BaseException):
    """Something went wrong with the FileStore"""


class BucketError(FileStoreError): ...


@dataclass
class BucketDoesNotExistError(FileStoreError):
    name: str

    def __str__(self) -> str:
        return self.name


class FileError(FileStoreError): ...


@dataclass
class CorruptFileError(FileError):
    """Our file was corrupt."""

    file_size: int  # in bytes
    min_size: int  # in bytes

    def __str__(self) -> str:
        return (
            f"file size ({self.file_size}) lower than minimum ({self.min_size} bytes)"
        )


@dataclass
class FileDoesNotExistError(FileError):
    filename: str

    def __str__(self) -> str:
        return self.filename
