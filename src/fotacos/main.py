"""Main entry point for fotacos application."""

import signal
import sys
from pathlib import Path

import click


def run_gui():
    """Run the Qt/QML GUI application."""
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine
    from PySide6.QtQuickControls2 import QQuickStyle

    # Allow Ctrl+C to close the application
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QGuiApplication(sys.argv)
    app.setOrganizationName("Maria")
    app.setApplicationName("Fotacos")

    QQuickStyle.setStyle("Material")

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    qml_file = Path(__file__).parent / "gui" / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


def run_web(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """Run the FastAPI web server."""
    import uvicorn

    uvicorn.run(
        "fotacos.api:app",
        host=host,
        port=port,
        reload=reload,
    )


@click.group()
@click.version_option(version="0.0.1")
def cli():
    """Fotacos - Photo Album Application."""


@cli.command()
def gui():
    """Run the desktop GUI application."""
    run_gui()


@cli.command()
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
