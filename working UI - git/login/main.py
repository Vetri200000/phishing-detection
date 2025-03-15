from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import jwt
import logging
import traceback
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 🔹 Use a strong secret key (Change this in production)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key", session_cookie="session_id")

# ✅ Google OAuth credentials
CLIENT_ID = "623565397438-56j4lk55qso3vcuosq10rpb4cosrv98n.apps.googleusercontent.com"
CLIENT_SECRET = ""
REDIRECT_URI = ""

# ✅ Serve static files (Your UI directory)
app.mount("/ui", StaticFiles(directory=r"C:\\Users\\vetri vel\\Desktop\\vetri phishing_Detection\\UI"), name="ui")

# ✅ Setup logging
logging.basicConfig(level=logging.DEBUG)

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
async def auth_callback(request: Request):
    """Handles Google authentication callback and stores user session in a text file"""
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

        # Log token response
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

        # 🔹 Store in a Text File
        file_path = "user_data.txt"  # Define file path
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"Name: {name}, Email: {email}\n")

        logging.info("User data saved to user_data.txt")

        # Redirect user back to home page
        return RedirectResponse(url="/ui/home.html")

    except Exception as e:
        logging.error("Error in auth_callback: %s", traceback.format_exc())
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)

@app.get("/api/user")
async def get_user(request: Request):
    """API to get logged-in user info from the session"""
    user_email = request.session.get("user_email")
    user_name = request.session.get("user_name")

    if not user_email or not user_name:
        return JSONResponse({"error": "User not logged in"}, status_code=401)
    
    return {"name": user_name, "email": user_email}