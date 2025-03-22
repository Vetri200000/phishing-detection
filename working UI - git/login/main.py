from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import jwt
import logging
import traceback
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from userdatabase import User, get_db, init_db  # Import ORM-related functions

app = FastAPI()

# 🔹 Use a strong secret key (Change this in production)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key", session_cookie="session_id")

# ✅ Google OAuth credentials
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-secret-id"
REDIRECT_URI = "http://localhost:8000/auth/callback"

# ✅ Serve static files (Your UI directory)
app.mount("/ui", StaticFiles(directory=r"D:\Git Repos\Project\phishing-detection\working UI - git"), name="ui")

# ✅ Setup logging
logging.basicConfig(level=logging.DEBUG)

# ✅ Initialize Database
init_db()

@app.get("/")
async def home():
    return RedirectResponse(url="/ui/home.html")

@app.get("/login")
async def login():
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=email profile openid"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    """Handles Google authentication callback and stores user in the database"""
    try:
        code = request.query_params.get("code")
        if not code:
            return JSONResponse({"error": "Authorization failed"}, status_code=400)

        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            tokens = response.json()

        logging.debug("Token response: %s", tokens)

        # Decode ID token to get user info
        id_token = tokens.get("id_token")
        if not id_token:
            return JSONResponse({"error": "Failed to retrieve ID token"}, status_code=400)

        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token.get("email")
        name = decoded_token.get("name")

        # Save user info in session
        request.session.update({
            "user_name": name,
            "user_email": email
        })

        # 🔹 Store in Database using ORM
        existing_user = db.query(User).filter(User.email == email).first()
        if not existing_user:
            new_user = User(name=name, email=email)
            db.add(new_user)
            db.commit()

        logging.info("User data saved to database")

        # Redirect user back to home page
        return RedirectResponse(url="/ui/home.html")

    except Exception as e:
        logging.error("Error in auth_callback: %s", traceback.format_exc())
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)

@app.get("/api/user")
async def get_user(request: Request, db: Session = Depends(get_db)):
    """API to get logged-in user info from the database"""
    user_email = request.session.get("user_email")

    if not user_email:
        return JSONResponse({"error": "User not logged in"}, status_code=401)

    user = db.query(User).filter(User.email == user_email).first()

    if user:
        return {"name": user.name, "email": user.email}
    else:
        return JSONResponse({"error": "User not found"}, status_code=404)
