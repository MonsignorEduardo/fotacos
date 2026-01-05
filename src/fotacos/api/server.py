"""Server startup for FastAPI application."""

import uvicorn

from fotacos.logging_config import setup_logging


def run_web(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    """Run the FastAPI web server."""
    # Setup logging before starting the server
    setup_logging()

    uvicorn.run(
        "fotacos.api:app",
        host=host,
        port=port,
        reload=reload,
        log_config=None,  # Disable uvicorn's logging config
        log_level=None,  # Prevent uvicorn from resetting log level
    )
