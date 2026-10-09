#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "==============================================="
echo " Building PinNote for macOS (.app & .dmg)"
echo "==============================================="

# Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller

# Clean old builds
rm -rf build dist/PinNote.app dist/PinNote-v1.0.dmg

# Build .app bundle with native icons and assets
pyinstaller --noconfirm --windowed \
    --name "PinNote" \
    --icon "assets/icon.icns" \
    --add-data "assets:assets" \
    --osx-bundle-identifier "com.pinnote.app" \
    pin_note.py

echo "Build successful! Created dist/PinNote.app"

# Package into .dmg if hdiutil is present (macOS built-in)
if command -v hdiutil &> /dev/null; then
    echo "Packaging into PinNote.dmg..."
    mkdir -p dmg_staging
    rm -rf dmg_staging/*
    cp -R "dist/PinNote.app" "dmg_staging/"
    ln -s /Applications "dmg_staging/Applications"
    
    rm -f "dist/PinNote-v1.0.dmg"
    hdiutil create -volname "PinNote" -srcfolder "dmg_staging" -ov -format UDZO "dist/PinNote-v1.0.dmg"
    rm -rf dmg_staging
    echo "==============================================="
    echo " DMG created successfully at dist/PinNote-v1.0.dmg"
    echo "==============================================="
fi
