from pizza_place_insights.logging import configure_logging

configure_logging()

__version__ = "0.0.2"

# Initialize DB models
from pizza_place_insights import models  # noqa: E402
