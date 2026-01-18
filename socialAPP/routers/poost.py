from fastapi import FASTAPIRouter

from socialAPP.models.post import UserPost, UserPostIn

router = FASTAPIRouter()


post_table = {}


@router.post("/", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post
