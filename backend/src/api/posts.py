from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from src.auth import AuthHandler
from src.models.post import BasePost, Post, PostWithTimestamp, get_post_with_timestamp

# FIXME: consider way to have this as singleton and not instantiate every time in different files
auth_handler = AuthHandler()

router = APIRouter(prefix="/posts")


@router.post("", status_code=201, response_model=PostWithTimestamp)
async def create_post(post: BasePost, user=Depends(auth_handler.write_authorized)):
    post = Post(
        username=user.username, title=post.title, content=post.content, votes=post.votes
    )
    await post.create()
    return get_post_with_timestamp(post)


@router.get(
    "",
    status_code=200,
    response_model=List[PostWithTimestamp],
    dependencies=[Depends(auth_handler.authorized)],
)
async def get_posts():
    return [get_post_with_timestamp(post) async for post in Post.find()]


@router.get(
    "/{id}",
    status_code=200,
    response_model=PostWithTimestamp,
    dependencies=[Depends(auth_handler.authorized)],
)
async def get_post(id):
    print(f"id: {id}")

    post = await Post.find_one(Post.id == PydanticObjectId(id))
    return get_post_with_timestamp(post)
