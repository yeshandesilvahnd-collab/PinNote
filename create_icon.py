import os
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PIL import Image

# Exact Royal Blue used in PinNote: #2563EB
# We use a refined modern gradient and sleek minimalist white geometry
SVG_ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <!-- Background Royal Blue Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="45%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>

    <!-- Subtle Inner Glow / Highlight -->
    <linearGradient id="highlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <!-- Note Card Shadow -->
    <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#0F172A" flood-opacity="0.35"/>
    </filter>

    <filter id="pinShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- 1. Squircle App Background in PinNote Royal Blue -->
  <rect x="24" y="24" width="464" height="464" rx="104" ry="104" fill="url(#bgGrad)" />
  <rect x="24" y="24" width="464" height="464" rx="104" ry="104" fill="url(#highlightGrad)" />
  <rect x="24" y="24" width="464" height="464" rx="104" ry="104" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="3"/>

  <!-- 2. Minimalist White Note Sheet with Rounded Corners & Shadow -->
  <g filter="url(#dropShadow)">
    <rect x="120" y="130" width="272" height="272" rx="36" ry="36" fill="#FFFFFF" fill-opacity="0.95"/>
    <!-- Subtle note lines -->
    <rect x="164" y="220" width="184" height="14" rx="7" fill="#2563EB" fill-opacity="0.25"/>
    <rect x="164" y="260" width="140" height="14" rx="7" fill="#2563EB" fill-opacity="0.20"/>
    <rect x="164" y="300" width="160" height="14" rx="7" fill="#2563EB" fill-opacity="0.15"/>
    <rect x="164" y="340" width="110" height="14" rx="7" fill="#2563EB" fill-opacity="0.12"/>
  </g>

  <!-- 3. Minimalist 3D/Flat Pushpin at Top of Note -->
  <g filter="url(#pinShadow)">
    <!-- Pin needle shadow & tip -->
    <path d="M256 180 L256 124" stroke="#94A3B8" stroke-width="12" stroke-linecap="round"/>
    
    <!-- Pushpin Head (Royal Blue & Bright Highlights) -->
    <!-- Base collar -->
    <rect x="220" y="112" width="72" height="20" rx="9" fill="#1D4ED8"/>
    <!-- Center waist -->
    <path d="M232 112 C232 86, 238 74, 246 64 L266 64 C274 74, 280 86, 280 112 Z" fill="#3B82F6"/>
    <!-- Top knob -->
    <ellipse cx="256" cy="62" rx="38" ry="16" fill="#60A5FA"/>
    <!-- Top glossy cap -->
    <ellipse cx="256" cy="58" rx="26" ry="10" fill="#93C5FD"/>
  </g>
</svg>'''

def generate_icons(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    svg_path = os.path.join(output_dir, "icon.svg")
    png_path = os.path.join(output_dir, "icon.png")
    ico_path = os.path.join(output_dir, "icon.ico")

    # 1. Save SVG
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(SVG_ICON)

    # 2. Render high-res PNG (512x512)
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(512, 512)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()
    pixmap.save(png_path, "PNG")

    # 3. Create Windows Multi-Size ICO using Pillow
    img = Image.open(png_path)
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format="ICO", sizes=ico_sizes)

    print("Icons successfully generated at:", output_dir)
    return svg_path, png_path, ico_path

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(curr_dir, "assets")
    generate_icons(assets_dir)
