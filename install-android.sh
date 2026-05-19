#!/bin/bash
# Atlas Data Toolkit — Android/Termux Installer
# curl -sL https://raw.githubusercontent.com/AtlasNexusTech/datatoolkit/master/install-android.sh | bash

set -e

echo "📦 Atlas Data Toolkit — Android Installer"
echo "========================================="

# Check if running in Termux
if [ -d /data/data/com.termux ]; then
    echo "✅ Termux detected"
    
    # Ensure Python
    if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
        echo "📥 Installing Python..."
        pkg install -y python
    fi
else
    echo "⚠️  Not running in Termux. This script is designed for Android/Termux."
    echo "   For Linux, use: pip install atlas-datatoolkit"
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)
echo "🐍 Python: $($PYTHON --version)"

# Download portable script
INSTALL_DIR="$HOME/.datatoolkit"
mkdir -p "$INSTALL_DIR"

echo "📥 Downloading datatoolkit..."
curl -sL "https://raw.githubusercontent.com/AtlasNexusTech/datatoolkit/master/datatoolkit-portable.py" -o "$INSTALL_DIR/datatoolkit"
curl -sL "https://raw.githubusercontent.com/AtlasNexusTech/datatoolkit/master/vendor/xmltodict.py" -o "$INSTALL_DIR/xmltodict.py"

chmod +x "$INSTALL_DIR/datatoolkit"

# Add to PATH via .bashrc
if ! grep -q "datatoolkit" ~/.bashrc 2>/dev/null; then
    echo "" >> ~/.bashrc
    echo "# Atlas Data Toolkit" >> ~/.bashrc
    echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> ~/.bashrc
    echo "alias dtk='python3 $INSTALL_DIR/datatoolkit'" >> ~/.bashrc
fi

echo ""
echo "✅ Installed!"
echo ""
echo "Usage:"
echo "  python3 $INSTALL_DIR/datatoolkit convert data.csv -o data.json"
echo "  dtk validate data.csv                    # (after restarting terminal)"
echo ""
echo "Restart Termux or run: source ~/.bashrc"
