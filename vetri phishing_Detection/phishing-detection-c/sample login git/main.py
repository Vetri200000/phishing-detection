from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
import jwt
import logging
import traceback
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Google OAuth credentials
CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
REDIRECT_URI = "http://localhost:8000/auth/callback"

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
            return {"error": "Authorization failed"}, 400

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

        # Log token response
        logging.debug("Token response: %s", tokens)

        # Decode ID token to get user info
        id_token = tokens.get("id_token")
        if not id_token:
            return {"error": "Failed to retrieve ID token"}, 400

        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token.get("email")
        name = decoded_token.get("name")

        # Save user info to a file
        with open("users.txt", "a") as file:
            file.write(f"{name} - {email}\n")

        # Store user info in session
        request.session["user_name"] = name
        request.session["user_email"] = email

        # Redirect user to dashboard
        return RedirectResponse(url="/dashboard")

    except Exception as e:
        logging.error("Error in auth_callback: %s", traceback.format_exc())
        return {"error": "Internal Server Error"}, 500

@app.get("/dashboard")
async def dashboard(request: Request):
    name = request.session.get("user_name", "Unknown User")
    email = request.session.get("user_email", "Unknown Email")
    return templates.TemplateResponse("dashboard.html", {"request": request, "name": name, "email": email})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
