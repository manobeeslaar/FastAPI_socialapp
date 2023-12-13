from fastapi import APIRouter, HTTPException

from socialapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()

posts = {}
comments = {}

def find_post(post_id: int):
    return posts.get(post_id)

@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(posts)
    new_post = {**data, "id": last_record_id}
    posts[last_record_id] = new_post
    return new_post

@router.get("/", response_model=list[UserPost])
async def get_posts():
    return list(posts.values())

@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.dict()
    last_record_id = len(comments)
    new_comment = {**data, "id": last_record_id}
    comments[last_record_id] = new_comment
    return new_comment

@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    return [
        comment
        for comment in comments.values()
        if comment['post_id'] == post_id
    ]
    
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }