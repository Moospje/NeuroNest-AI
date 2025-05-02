from fastapi import APIRouter

from api.v1.endpoints import auth, users, agents, conversations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])