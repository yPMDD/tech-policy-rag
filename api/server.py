from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api.routes import chat
from api.auth import oauth_handler
from api.database.session import engine
from api.models.database_models import Base
import os

# Create database tables if they don't exist
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")
except Exception as e:
    print(f"Warning: Could not initialize database tables. Ensure Postgres is running. Error: {e}")

app = FastAPI(title="Tech Policy RAG API")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Be specific for cookies
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Required for Authlib/Starlette to handle the session cookie across ports
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("JWT_SECRET", "supersecret"),
    same_site="lax", 
    https_only=False
)

# Allow insecure transport for OAuth in development (REQUIRED for http://localhost)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Routes
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(oauth_handler.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Tech Policy RAG API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
