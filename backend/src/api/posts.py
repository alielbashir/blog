from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.auth import auth_handler
from src.models.post import BasePost, Post, PostWithTimestamp, get_post_with_timestamp
from src.models.user import UserNoPass

router = APIRouter(prefix="/posts")


@router.post("", status_code=201, response_model=PostWithTimestamp)
async def create_post(post: BasePost, user=Depends(auth_handler.write_authorized)):
    post = Post(username=user.username, title=post.title, content=post.content)
    await post.create()
    return get_post_with_timestamp(post, requester_username=user.username)


@router.get(
    "",
    status_code=200,
    response_model=List[PostWithTimestamp],
    dependencies=[Depends(auth_handler.authorized)],
)
async def get_posts(user=Depends(auth_handler.authorized)):
    return [
        get_post_with_timestamp(post, requester_username=user.username)
        async for post in Post.find_all()
    ]


@router.get(
    "/{id}",
    status_code=200,
    response_model=PostWithTimestamp,
    dependencies=[Depends(auth_handler.authorized)],
)
async def get_post(id, user=Depends(auth_handler.authorized)):
    print(f"id: {id}")

    post = await Post.get(id)
    return get_post_with_timestamp(post, requester_username=user.username)


@router.post(
    "/{post_id}/upvote",
    status_code=200,
    response_model=PostWithTimestamp,
)
async def upvote_post(
    post_id: str, user: UserNoPass = Depends(auth_handler.authorized)
):
    """Upvotes a post, if already upvoted then undos upvote"""
    # find post
    post = await Post.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if user.username in post.upvoters:
        # undo upvote
        post.upvoters.remove(user.username)
        post.votes -= 1
    elif user.username in post.downvoters:
        # undo downvote and then upvote
        post.downvoters.remove(user.username)
        post.upvoters.append(user.username)
        post.votes += 2
    else:
        # upvote
        post.upvoters.append(user.username)
        post.votes += 1

    await post.save()

    print(f"downvoters = {post.downvoters}")
    print(f"upvoters = {post.upvoters}")
    new_post = get_post_with_timestamp(post, requester_username=user.username)
    print(f"new_post: {new_post}")
    return new_post


@router.post(
    "/{post_id}/downvote",
    status_code=200,
    response_model=PostWithTimestamp,
)
async def downvote_post(
    post_id: str, user: UserNoPass = Depends(auth_handler.authorized)
):
    """downvotes a post, if already downvoted then undos downvote"""
    # find post
    post = await Post.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if user.username in post.downvoters:
        # undo downvote
        post.downvoters.remove(user.username)
        post.votes += 1
    elif user.username in post.upvoters:
        # undo upvote and then downvote
        post.upvoters.remove(user.username)
        post.downvoters.append(user.username)
        post.votes -= 2
    else:
        # downvote
        post.downvoters.append(user.username)
        post.votes -= 1

    await post.save()
    print(f"downvoters = {post.downvoters}")
    print(f"upvoters = {post.upvoters}")
    new_post = get_post_with_timestamp(post, requester_username=user.username)
    print(f"new_post: {new_post}")
    return new_post
