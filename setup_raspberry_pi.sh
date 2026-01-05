#!/bin/bash
# Setup script for Fotacos on Raspberry Pi 5
# This script installs system dependencies and the Fotacos application

set -e  # Exit on error

echo "========================================="
echo "Fotacos - Raspberry Pi 5 Setup"
echo "========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Updating system packages..."
sudo apt-get update

echo ""
echo "📦 Installing system dependencies for Qt/PySide6..."
sudo apt-get install -y \
    curl \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6core6 \
    libqt6qml6 \
    libqt6quick6 \
    qt6-qpa-plugins \
    qml6-module-qtquick \
    qml6-module-qtquick-controls \
    qml6-module-qtquick-layouts \
    qml6-module-qtquick-window \
    libxcb-cursor0 \
    libxcb-xinerama0

echo ""
echo "🚀 Installing uv (Python package manager)..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
else
    echo "✓ uv is already installed"
fi

echo ""
echo "📦 Installing Fotacos from wheel file..."
WHEEL_FILE=$(find . -name "fotacos-*.whl" | head -n 1)

if [ -z "$WHEEL_FILE" ]; then
    echo "❌ Error: No wheel file found in current directory"
    echo "Please place the fotacos-*.whl file in this directory"
    exit 1
fi

echo "Found wheel file: $WHEEL_FILE"

# Create uv project and install
uv venv
uv pip install "$WHEEL_FILE"

echo ""
echo "✅ Installation complete!"
echo ""
echo "========================================="
echo "How to run Fotacos:"
echo "========================================="
echo ""
echo "1. Run the GUI application:"
echo "   uv run fotacos gui"
echo ""
echo "2. Or run the web server (API + Web interface):"
echo "   uv run fotacos server"
echo ""
echo "========================================="
echo "Optional: Auto-start GUI on boot"
echo "========================================="
echo ""
read -p "Do you want to set up GUI auto-start on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./setup_autostart.sh
fi

echo ""
echo "✨ Setup complete! Enjoy your photo gallery!"
