from fastapi import APIRouter

from api.v1.record.controller import router as record_router
from api.v1.user.controller import router as user_router

router = APIRouter()

router.include_router(record_router)
router.include_router(user_router)
