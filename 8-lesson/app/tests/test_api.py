import pytest

@pytest.mark.asyncio
async def test_read_news(async_client):
    response = await async_client.get("/news")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_news(async_client, auth_headers):
    payload = {"title": "Test News", "content": "Content", "is_published": True}
    response = await async_client.post("/news", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test News"

@pytest.mark.asyncio
async def test_update_news(async_client, auth_headers):
    # Tạo
    create = await async_client.post("/news", json={"title": "Old", "content": "c"}, headers=auth_headers)
    nid = create.json()["id"]
    
    # Sửa
    res = await async_client.put(f"/news/{nid}", json={"title": "New", "content": "c"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "New"

@pytest.mark.asyncio
async def test_delete_news(async_client, auth_headers):
    # Tạo
    create = await async_client.post("/news", json={"title": "Del", "content": "c"}, headers=auth_headers)
    nid = create.json()["id"]
    
    # Xóa
    res = await async_client.delete(f"/news/{nid}", headers=auth_headers)
    assert res.status_code == 200