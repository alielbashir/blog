from typing import List

from beanie import Document
from pydantic import BaseModel


class BasePost(BaseModel):
    """A post entered by the user"""

    title: str
    content: str
    votes: int = 0


class Post(Document, BasePost):
    """A post saved in the database"""

    username: str
    upvoters: List[str] = []
    downvoters: List[str] = []


class PostWithTimestamp(BasePost):
    """A post returned to the user with a timestamp and id"""

    id: str
    creation_date: int


def get_post_with_timestamp(post: Post):
    return PostWithTimestamp(
        id=str(post.id),
        username=post.username,
        title=post.title,
        content=post.content,
        creation_date=int(post.id.generation_time.timestamp()),
        votes=post.votes,
    )
