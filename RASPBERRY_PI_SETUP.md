# Fotacos - Raspberry Pi 5 Setup Guide

## Prerequisites

- Raspberry Pi 5 with Raspberry Pi OS (64-bit recommended)
- Internet connection for downloading dependencies
- Display connected (for GUI mode)
- The `fotacos-0.0.1-py3-none-any.whl` file

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Transfer the wheel file to your Raspberry Pi:**
   ```bash
   scp fotacos-0.0.1-py3-none-any.whl pi@raspberrypi.local:~/fotacos/
   scp setup_raspberry_pi.sh pi@raspberrypi.local:~/fotacos/
   scp setup_autostart.sh pi@raspberrypi.local:~/fotacos/
   ```

2. **SSH into your Raspberry Pi:**
   ```bash
   ssh pi@raspberrypi.local
   cd ~/fotacos
   ```

3. **Make scripts executable:**
   ```bash
   chmod +x setup_raspberry_pi.sh setup_autostart.sh
   ```

4. **Run the setup script:**
   ```bash
   ./setup_raspberry_pi.sh
   ```

   This will:
   - Install system dependencies (Qt libraries, Python packages)
   - Create a Python virtual environment
   - Install the wheel file and all Python dependencies automatically
   - Optionally configure auto-start on boot

### Method 2: Manual Installation

1. **Install system dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y curl \
       libqt6gui6 libqt6widgets6 libqt6core6 libqt6qml6 libqt6quick6 \
       qt6-qpa-plugins qml6-module-qtquick qml6-module-qtquick-controls \
       qml6-module-qtquick-layouts qml6-module-qtquick-window \
       libxcb-cursor0 libxcb-xinerama0
   ```

2. **Install uv (Python package manager):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.cargo/env
   ```

3. **Create virtual environment and install the wheel file:**
   ```bash
   uv venv
   uv pip install fotacos-0.0.1-py3-none-any.whl
   ```

   **Note:** The wheel file contains metadata about all Python dependencies. When you install it with `uv pip`, it will automatically download and install all required Python packages (fastapi, pyside6, pillow, tortoise-orm, etc.) from PyPI. `uv` is significantly faster than traditional pip.

## Running Fotacos

### GUI Mode (Photo Slideshow)

```bash
uv run fotacos gui
```

Features:
- Fullscreen photo slideshow
- Auto-advance every 30 seconds
- Touch-friendly navigation buttons
- Swipe gestures for navigation
- Double-tap to access gallery grid view

### Server Mode (API + Web Interface)

```bash
uv run fotacos server
```

Then access the web interface at:
- Local: `http://localhost:8000`
- Network: `http://raspberrypi.local:8000`

## Auto-Start on Boot

To run the GUI automatically when Raspberry Pi boots:

```bash
./setup_autostart.sh
```

Or manually:

```bash
sudo systemctl enable fotacos
sudo systemctl start fotacos
```

Manage the service:
```bash
# Check status
sudo systemctl status fotacos

# Stop service
sudo systemctl stop fotacos

# View logs
journalctl -u fotacos -f

# Disable auto-start
sudo systemctl disable fotacos
```

## Upload Photos

### From Web Interface

1. Access `http://raspberrypi.local:8000` from any device on your network
2. Click "Subir Foto" (Upload Photo)
3. Select image files (jpg, png, gif, webp, bmp)
4. Photos are automatically converted to WebP and thumbnails generated

### Directly to Filesystem

Upload photos to the `public/picts/` directory and they'll appear in the gallery after refreshing.

## Troubleshooting

### GUI doesn't start

1. **Check display environment:**
   ```bash
   echo $DISPLAY
   # Should output :0 or :0.0
   ```

2. **Set display manually:**
   ```bash
   export DISPLAY=:0
   fotacos gui
   ```
uv run fotacos gui
   ```

3. **Check Qt platform:**
   ```bash
   export QT_QPA_PLATFORM=xcb
   uv run
### Permission errors

```bash
sudo chown -R $USER:$USER ~/fotacos
chmod -R 755 ~/fotacos
```

### Database locked errors

Make sure only one instance of Fotacos is running:
```bash
pkill -f fotacos
```

### Out of memory

Reduce thumbnail size in settings or use lighter image formats.

## Performance Tips for Raspberry Pi

1. **Use WebP format** - Already automatic via upload
2. **Limit photo resolution** - Consider resizing large images
3. **Enable GPU acceleration:**
   ```bash
   sudo raspi-config
   # Advanced Options > GL Driver > GL (Full KMS)
   ```
4. **Overclock (optional)** - Via `raspi-config` > Performance Options

## File Locations

- **Virtual Environment:** `~/fotacos/.venv/`
- **uv binary:** `~/.cargo/bin/uv`
- **Photos:** `~/fotacos/public/picts/`
- **Thumbnails:** `~/fotacos/public/picts/thumbnails/`
- **Database:** `~/fotacos/fotacos.db`
- **Logs:** `~/fotacos/logs/`
- **Service:** `/etc/systemd/system/fotacos.service`

## Uninstallation

```bash
# Stop and disable service (if configured)
sudo systemctl stop fotacos
sudo systemctl disable fotacos
sudo rm /etc/systemd/system/fotacos.service

# Remove installation
rm -rf ~/fotacos

# Remove system packages (optional)
sudo apt-get remove --autoremove \
    libqt6gui6 libqt6widgets6 libqt6core6 libqt6qml6 libqt6quick6
```

## Hardware Recommendations

- **Display:** 7" or larger touchscreen for best experience
- **Storage:** microSD card 32GB+ or SSD via USB 3.0
- **Power:** Official Raspberry Pi 5 power supply (5V 5A)
- **Case:** With cooling fan for continuous operation

## Support

For issues, check the logs:
```bash
journalctl -u fotacos -f  # If running as service
cat ~/fotacos/logs/app.log  # Application logs
```
