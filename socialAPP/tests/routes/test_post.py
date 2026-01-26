import pytest
import pytest_asyncio
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post/", json={"body": body})
    return response.json()

async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/post/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()

@pytest_asyncio.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post Body", async_client)

@pytest_asyncio.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test Comment Body", created_post["id"], async_client)

@pytest.mark.asyncio
async def test_create_post(async_client: AsyncClient):
    body = "This is a test post"
    response = await async_client.post("/post/", json={"body": body})
    assert response.status_code == 201
    assert {"id": 0, "body": body}.items() <= response.json().items()

@pytest.mark.asyncio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/post/", json={})
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post/post")
    assert response.status_code == 200
    #posts = response.json()
    assert response.json() == [created_post]
    #assert any(post["id"] == created_post["id"] for post in posts)

@pytest.mark.asyncio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "This is a test comment"
    response = await async_client.post(
        "/post/comment", json={"body": body, "post_id": created_post["id"]}
    )
    assert response.status_code == 201
    assert {"id": 0, "body": body, "post_id": created_post["id"]}.items() <= response.json().items()

@pytest.mark.asyncio
async def test_get_comments_for_post(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/post/post/{created_post['id']}/comment")
    assert response.status_code == 200
    assert response.json() == [created_comment]
    #assert any(comment["id"] == created_comment["id"] for comment in comments)