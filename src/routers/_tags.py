from dataclasses import asdict, dataclass

TAGS_METADATA: list[dict[str, str]] = []
"""Metadata for tags, used for OpenAPI documentation"""
# More details https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags


@dataclass
class _Tag:
    """Tag metadata for OpenAPI documentation"""

    name: str
    description: str

    def __post_init__(self):
        global TAGS_METADATA
        TAGS_METADATA.append(asdict(self))


V1 = _Tag("V1", "Version 1 of the API").name
FOO = _Tag("Foo", "Foo description").name
