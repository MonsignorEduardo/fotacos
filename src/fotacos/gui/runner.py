"""GUI application runner."""

import asyncio
import signal
import sys
from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal, Slot
from qasync import QEventLoop

from fotacos.database import close_db, init_db
from fotacos.env import get_settings
from fotacos.models.photo import Photo


class PhotoGalleryModel(QObject):
    """Model to expose photos to QML."""

    photosChanged = Signal()

    def __init__(self) -> None:
        """Initialize the photo gallery model."""
        super().__init__()
        self._photos: list[dict] = []
        self._settings = get_settings()
        self._tasks: set = set()

    @Property(list, notify=photosChanged)
    def photos(self) -> list[dict]:
        """Get the list of photos."""
        return self._photos

    async def load_photos(self) -> None:
        """Load photos from the database."""
        # Fetch all photos ordered by newest first
        photo_records = await Photo.all().order_by("-created_at")

        # Convert to list of dicts with absolute file paths for QML
        self._photos = []
        for photo in photo_records:
            # Convert database URL path to absolute filesystem path
            # Database stores: "/public/picts/filename.webp"
            # We need: "file:///absolute/path/to/public/picts/filename.webp"
            relative_path = photo.original_url.lstrip("/")
            absolute_path = (Path.cwd() / relative_path).resolve()

            self._photos.append({
                "id": photo.id,
                "filename": photo.filename,
                "path": f"file://{absolute_path}",
                "createdAt": photo.created_at.isoformat() if photo.created_at else "",
            })

        self.photosChanged.emit()

    @Slot()
    def refresh(self) -> None:
        """Refresh photos from database (callable from QML)."""
        task = asyncio.create_task(self.load_photos())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)


def run_gui() -> None:
    """Run the Qt/QML GUI application."""
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine
    from PySide6.QtQuickControls2 import QQuickStyle

    # Allow Ctrl+C to close the application
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QGuiApplication(sys.argv)
    app.setOrganizationName("Maria")
    app.setApplicationName("Fotacos")

    # Set up async event loop for Qt
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    QQuickStyle.setStyle("Material")

    # Initialize database
    loop.run_until_complete(init_db())

    # Create and setup the photo gallery model
    gallery_model = PhotoGalleryModel()

    # Load photos before starting the UI
    loop.run_until_complete(gallery_model.load_photos())

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    # Make the model available to QML
    engine.rootContext().setContextProperty("galleryModel", gallery_model)

    qml_file = Path(__file__).parent / "ui" / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        loop.run_until_complete(close_db())
        sys.exit(-1)

    try:
        exit_code = loop.run_forever()
    finally:
        loop.run_until_complete(close_db())
        loop.close()

    del engine
    sys.exit(exit_code if isinstance(exit_code, int) else 0)
