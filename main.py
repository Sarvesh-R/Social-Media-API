from fastapi import FastAPI
from db import create_tables
from routers import auth, follower, posts, comments, user

# --------------------------------------------------------
# INITIALIZE FASTAPI APPLICATION
# --------------------------------------------------------
app = FastAPI(
    title="Social Media API",
    version="1.0.0",
    description="API for managing users, posts, comments, and authentication features in a social media platform."
)

# --------------------------------------------------------
# CREATE DATABASE TABLES ON STARTUP (OPTIONAL)
# --------------------------------------------------------
# create_tables()

# --------------------------------------------------------
# HEALTH CHECK ENDPOINT
# --------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "API is running"}

# --------------------------------------------------------
# REGISTER API ROUTERS
# --------------------------------------------------------
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(follower.router, prefix="/api/v1/users", tags=["Followers"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/api/v1", tags=["Comments"])
