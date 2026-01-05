#!/bin/bash
# Setup Fotacos GUI to start automatically on Raspberry Pi boot

set -e

echo "🚀 Setting up Fotacos GUI auto-start..."

# Get the absolute path to uv and the project directory
UV_BIN="$HOME/.cargo/bin/uv"
PROJECT_DIR="$(pwd)"

if [ ! -f "$UV_BIN" ]; then
    echo "❌ Error: uv not found at $UV_BIN"
    echo "Please run setup_raspberry_pi.sh first"
    exit 1
fi

if [ ! -d "$PROJECT_DIR/.venv" ]; then
    echo "❌ Error: Virtual environment not found at $PROJECT_DIR/.venv"
    echo "Please run setup_raspberry_pi.sh first"
    exit 1
fi

# Create systemd service file
echo "📝 Creating systemd service..."
sudo tee /etc/systemd/system/fotacos.service > /dev/null <<EOF
[Unit]
Description=Fotacos Photo Gallery GUI
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
User=$USER
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/$(id -u)
Environment=QT_QPA_PLATFORM=xcb
Environment=PATH=$HOME/.cargo/bin:/usr/local/bin:/usr/bin:/bin
WorkingDirectory=$PROJECT_DIR
ExecStart=$UV_BIN run fotacos gui
Restart=on-failure
RestartSec=10

[Install]
WantedBy=graphical.target
EOF

# Enable and start the service
echo "🔧 Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable fotacos.service

echo ""
echo "✅ Auto-start configured!"
echo ""
echo "Useful commands:"
echo "  Start:   sudo systemctl start fotacos"
echo "  Stop:    sudo systemctl stop fotacos"
echo "  Status:  sudo systemctl status fotacos"
echo "  Disable: sudo systemctl disable fotacos"
echo "  Logs:    journalctl -u fotacos -f"
echo ""
read -p "Start the service now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo systemctl start fotacos
    echo "🎉 Fotacos GUI is now running!"
    echo "Check status with: sudo systemctl status fotacos"
fi
