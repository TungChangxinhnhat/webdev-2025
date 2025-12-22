import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"

def test_news_crud_flow(page: Page):
    page.request.post(f"{BASE_URL}/auth/register", data={"username": "uiuser", "password": "uipassword"})

    # 1. Login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "uiuser")
    page.fill('input[name="password"]', "uipassword")
    page.click('button:has-text("Login")')
    
    # Chờ vào trang list
    expect(page).to_have_url(f"{BASE_URL}/news-ui")

    # 2. CREATE
    page.click('text="Create News"')
    page.fill('input[name="title"]', "E2E News")
    page.fill('textarea[name="content"]', "Content E2E")
    page.click('button:has-text("Submit")')
    
    # Check đã hiện tin
    expect(page.get_by_text("E2E News")).to_be_visible()

    # 3. UPDATE
    page.click('text="Edit"') 
    page.fill('input[name="title"]', "E2E Updated")
    page.click('button:has-text("Save")')
    
    expect(page.get_by_text("E2E Updated")).to_be_visible()

    # 4. DELETE
    page.click('button:has-text("Delete")')
    expect(page.get_by_text("E2E Updated")).not_to_be_visible()