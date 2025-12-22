import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

users_db = {}
news_db = []
tokens_db = {}

class UserRegister(BaseModel):
    username: str
    password: str

class NewsItem(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    is_published: bool = True

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    for user, t in tokens_db.items():
        if t == token:
            return user
    raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/auth/register")
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.password
    return {"message": "Registered successfully"}

@app.post("/auth/jwt/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_pass = users_db.get(form_data.username)
    if not user_pass or user_pass != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = f"{form_data.username}_token"
    tokens_db[form_data.username] = token
    return {"access_token": token, "token_type": "bearer"}

@app.get("/news", response_model=List[NewsItem])
def get_news():
    return news_db

@app.post("/news", status_code=201)
def create_news(news: NewsItem, user: str = Depends(get_current_user)):
    news.id = str(uuid.uuid4())
    news_db.append(news)
    return news

@app.put("/news/{news_id}")
def update_news(news_id: str, news_update: NewsItem, user: str = Depends(get_current_user)):
    for news in news_db:
        if news.id == news_id:
            news.title = news_update.title
            news.content = news_update.content
            return news
    raise HTTPException(status_code=404, detail="News not found")

@app.delete("/news/{news_id}")
def delete_news(news_id: str, user: str = Depends(get_current_user)):
    global news_db
    news_db = [n for n in news_db if n.id != news_id]
    return {"message": "Deleted"}

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
        <body>
            <h1>Login</h1>
            <form action="/login" method="post">
                <input name="username" placeholder="Username">
                <input name="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """

@app.post("/login")
def login_submit(username: str = Form(...), password: str = Form(...)):
    if username in users_db and users_db[username] == password:
        return RedirectResponse(url="/news-ui", status_code=303)
    return HTMLResponse("Login failed", status_code=400)

@app.get("/news-ui", response_class=HTMLResponse)
def news_ui():
    html = """<h1>News List</h1> <a href='/news/create'>Create News</a><ul>"""
    for n in news_db:
        html += f"""
            <li>
                <span>{n.title}</span> - {n.content}
                <a href='/news/edit/{n.id}'>Edit</a>
                <form action='/news/delete/{n.id}' method='post' style='display:inline'>
                    <button type="submit">Delete</button>
                </form>
            </li>
        """
    html += "</ul>"
    return HTMLResponse(html)

@app.get("/news/create", response_class=HTMLResponse)
def create_news_ui():
    return """
    <h1>Create News</h1>
    <form action="/news/create" method="post">
        <input name="title" placeholder="Title">
        <textarea name="content" placeholder="Content"></textarea>
        <button type="submit">Submit</button>
    </form>
    """

@app.post("/news/create")
def create_news_submit(title: str = Form(...), content: str = Form(...)):
    new_item = NewsItem(id=str(uuid.uuid4()), title=title, content=content)
    news_db.append(new_item)
    return RedirectResponse(url="/news-ui", status_code=303)

@app.get("/news/edit/{news_id}", response_class=HTMLResponse)
def edit_news_ui(news_id: str):
    news = next((n for n in news_db if n.id == news_id), None)
    if not news: return HTMLResponse("Not found", 404)
    return f"""
    <h1>Edit News</h1>
    <form action="/news/edit/{news_id}" method="post">
        <input name="title" value="{news.title}">
        <button type="submit">Save</button>
    </form>
    """

@app.post("/news/edit/{news_id}")
def edit_news_submit(news_id: str, title: str = Form(...)):
    for n in news_db:
        if n.id == news_id:
            n.title = title
    return RedirectResponse(url="/news-ui", status_code=303)

@app.post("/news/delete/{news_id}")
def delete_news_submit(news_id: str):
    global news_db
    news_db = [n for n in news_db if n.id != news_id]
    return RedirectResponse(url="/news-ui", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)