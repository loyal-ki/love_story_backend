from fastapi import APIRouter
from src.constants.constants import API_PREFIX
from src.routers.auth.auth_route import router as users_route
from src.routers.otps.otps_route import router as otps_route

routers = APIRouter()

# authorization
routers.include_router(users_route, prefix=f"{API_PREFIX}/auth", tags=["Auth"])
#
routers.include_router(otps_route, prefix=f"{API_PREFIX}/otps", tags=["OTPs"])
