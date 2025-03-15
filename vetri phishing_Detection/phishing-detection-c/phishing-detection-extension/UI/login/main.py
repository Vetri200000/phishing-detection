from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import jwt
import logging
import traceback
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Google OAuth credentials
CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CLIENT_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
REDIRECT_URI = "http://localhost:8000/auth/callback"

# Serve static files (your UI directory)
app.mount("/ui", StaticFiles(directory="C:/Users/vetri vel/Desktop/vetri phishing_Detection/phishing-detection-c/phishing-detection-extension/UI"), name="ui")


# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.get("/")
async def home():
    return RedirectResponse(url="/login")

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
async def auth_callback(request: Request):
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

        # Decode ID token to get user info
        id_token = tokens.get("id_token")
        if not id_token:
            return JSONResponse({"error": "Failed to retrieve ID token"}, status_code=400)

        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token.get("email")
        name = decoded_token.get("name")

        # Store user info in session
        request.session["user_name"] = name
        request.session["user_email"] = email

        logging.debug(f"Session Data Stored: Name={name}, Email={email}")

        return RedirectResponse(url="/ui/home.html")

    except Exception as e:
        logging.error("Error in auth_callback: %s", traceback.format_exc())
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)

@app.get("/api/user")
async def get_user_info(request: Request):
    """Fetch logged-in user's name and email from session."""
    name = request.session.get("user_name")
    email = request.session.get("user_email")

    logging.debug(f"Session Retrieved: Name={name}, Email={email}")

    if not name or not email:
        return JSONResponse({"name": "Guest", "email": "Not logged in"})

    return JSONResponse({"name": name, "email": email})
