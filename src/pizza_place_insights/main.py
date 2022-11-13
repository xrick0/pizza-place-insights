import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pizza_place_insights
from pizza_place_insights import api
from pizza_place_insights.config import get_settings

log = logging.getLogger(__name__)


swagger_ui_parameters = {
    "displayRequestDuration": True,
    "filter": True,
    "syntaxHighlight.theme": "arta",
}

log.debug("Initializing FastAPI instance")
app = FastAPI(
    title="API",
    description="",
    version=pizza_place_insights.__version__,
    swagger_ui_parameters=swagger_ui_parameters,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/health_check")
def health_check() -> dict[str, str]:
    """API health check endpoint"""

    return {"ping": "pong"}


app.include_router(api.router)
