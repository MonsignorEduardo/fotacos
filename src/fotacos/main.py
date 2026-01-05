"""Main entry point for fotacos application."""

import click

from fotacos.api import run_web


@click.group()
@click.version_option(version="0.0.1")
def cli():
    """Fotacos - Photo Album Application."""


@cli.command()
def gui():
    """Run the desktop GUI application."""
    # Lazy import to avoid Qt dependencies when not needed
    from fotacos.gui import run_gui

    run_gui()


@click.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, type=int, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
def web(host: str, port: int, reload: bool):
    """Run the web server."""
    run_web(host=host, port=port, reload=reload)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
