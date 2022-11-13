from fastapi import APIRouter

from pizza_place_insights.services.uploads.orders.router import router as orders_router
from pizza_place_insights.services.uploads.pizza_types.router import router as pizza_types_router
from pizza_place_insights.services.uploads.pizzas.router import router as pizzas_router

router = APIRouter(prefix="/upload")

router.include_router(pizza_types_router)
router.include_router(pizzas_router)
router.include_router(orders_router)
