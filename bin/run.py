import uvicorn
from pizza_place_insights.config import get_settings

if __name__ == "__main__":
    uvicorn.run(
        "pizza_place_insights.main:app",
        host=get_settings().app_host,
        port=get_settings().app_port,
        reload=get_settings().dev_uvicorn_reload,
    )
