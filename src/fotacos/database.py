"""Database configuration and initialization."""

from tortoise import Tortoise

from fotacos.env import get_settings


async def init_db() -> None:
    """Initialize Tortoise ORM and generate schema."""
    settings = get_settings()

    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["fotacos.models.photo"]},
    )
    await Tortoise.generate_schemas()


async def close_db() -> None:
    """Close database connections."""
    await Tortoise.close_connections()
