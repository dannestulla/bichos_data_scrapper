from dataclasses import dataclass
from typing import List


def post_pictures_serializer(obj):
    if isinstance(obj, (Images, PostImages)):
        return obj.__dict__
    raise TypeError(f"Objeto do tipo {type(obj).__name__} não é serializável")


@dataclass
class Images:
    image: str


@dataclass
class PostImages:
    page: str
    images: List[Images]
