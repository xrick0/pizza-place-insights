from fastapi import APIRouter

from pizza_place_insights.services.uploads.pizza_types.router import router as pizza_types_router

router = APIRouter(prefix="/upload")

router.include_router(pizza_types_router)
