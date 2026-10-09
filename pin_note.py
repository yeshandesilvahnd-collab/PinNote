"""
PinNote - Minimalist Modern Sticky Note with Reboot Persistence,
Always-on-Top Toggle, Rich Text & Table Formatting, and Dark/Light Modes.
"""

import sys
import os
import re
import html
import base64
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QSizeGrip, QFrame, QMenu,
    QCheckBox, QDialog, QSpinBox, QDialogButtonBox, QFormLayout,
    QComboBox, QSlider, QFileDialog
)
from PyQt6.QtCore import (
    Qt, QPoint, QTimer, QSize, QRect, QEvent, QPropertyAnimation,
    QByteArray, QBuffer, QIODevice, QMimeData, QUrl
)
from PyQt6.QtGui import (
    QFont, QTextCursor, QTextDocumentFragment, QTextDocument, QColor,
    QKeySequence, QShortcut, QTextTableFormat, QTextLength,
    QIcon, QPixmap, QPainter, QTextCharFormat, QAction, QActionGroup,
    QCursor, QImage, QPen, QBrush
)
from PyQt6.QtSvg import QSvgRenderer

from storage import (
    load_data,
    save_data,
    set_start_on_boot,
    is_start_on_boot_enabled,
)

def get_asset_path(filename: str) -> str:
    """Resolve asset path whether running as script or frozen PyInstaller exe."""
    if getattr(sys, "frozen", False):
        base_exe = os.path.dirname(sys.executable)
        p = os.path.join(base_exe, "assets", filename)
        if os.path.exists(p):
            return p
        if hasattr(sys, "_MEIPASS"):
            p = os.path.join(sys._MEIPASS, "assets", filename)
            if os.path.exists(p):
                return p
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "assets", filename)

MOD_KEY = "Cmd" if sys.platform == "darwin" else "Ctrl"

def get_app_font(size: int = 10, bold: bool = False) -> QFont:
    """Return system-native crisp font (Apple system font on macOS, Segoe UI on Windows)."""
    family = ".AppleSystemUIFont" if sys.platform == "darwin" else "Segoe UI"
    font = QFont(family, size)
    if bold:
        font.setWeight(QFont.Weight.Bold)
    return font

# ----------------- Minimalist Vector SVG Icons -----------------
SVGS = {
    "copy": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect width="13" height="13" x="8" y="8" rx="2" ry="2"/>'
        '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'
        '</svg>'
    ),
    "trash": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 6h18"/>'
        '<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>'
        '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>'
        '<line x1="10" x2="10" y1="11" y2="17"/>'
        '<line x1="14" x2="14" y1="11" y2="17"/>'
        '</svg>'
    ),
    "moon": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
        '</svg>'
    ),
    "sun": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>'
        '</svg>'
    ),
    "pin": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="12" x2="12" y1="17" y2="22"/>'
        '<path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/>'
        '</svg>'
    ),
    "pin_active": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="#2563EB" stroke="#2563EB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="12" x2="12" y1="17" y2="22" stroke-width="2.2"/>'
        '<path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/>'
        '</svg>'
    ),
    "minimize": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
        '<line x1="5" y1="12" x2="19" y2="12"/>'
        '</svg>'
    ),
    "maximize": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect width="14" height="14" x="5" y="5" rx="1.5"/>'
        '</svg>'
    ),
    "restore": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect width="11" height="11" x="4" y="9" rx="1.5"/>'
        '<path d="M8 5h9a2 2 0 0 1 2 2v9"/>'
        '</svg>'
    ),
    "close": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="18" y1="6" x2="6" y2="18"/>'
        '<line x1="6" y1="6" x2="18" y2="18"/>'
        '</svg>'
    ),
    "settings": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>'
        '<circle cx="12" cy="12" r="3"/>'
        '</svg>'
    ),
}

def render_svg_icon(svg_key: str, color: str = "#A1A1AA", size: int = 14) -> QIcon:
    """Render anti-aliased, crisp high-DPI icon from SVG string."""
    svg_str = SVGS.get(svg_key, "").replace("currentColor", color)
    r = QSvgRenderer(svg_str.encode("utf-8"))
    scale = 2  # 2x supersampling for retina/high-DPI sharpness
    p = QPixmap(size * scale, size * scale)
    p.fill(Qt.GlobalColor.transparent)
    painter = QPainter(p)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    r.render(painter)
    painter.end()
    return QIcon(p)


# ----------------- Color Schemes -----------------
THEMES = {
    "dark": {
        "bg": "#18181B",            # Zinc 900
        "title_bg": "#18181B",
        "card_bg": "#222226",       # Zinc 800-ish
        "border": "#2E2E33",
        "text": "#F4F4F5",
        "text_muted": "#A1A1AA",
        "btn_hover": "rgba(255, 255, 255, 0.08)",
        "accent": "#2563EB",        # Royal Blue
        "accent_bg": "rgba(37, 99, 235, 0.2)",
        "success": "#10B981",       # Emerald
        "danger": "#EF4444",
        "banner_bg": "#312E81",
        "banner_text": "#E0E7FF",
        "table_border": "#52525B",
        "table_header_bg": "#2E2E33",
        "table_alt_bg": "#1E1E22",
        "scrollbar": "#3F3F46",
    },
    "light": {
        "bg": "#F8FAFC",            # Slate 50
        "title_bg": "#F8FAFC",
        "card_bg": "#FFFFFF",
        "border": "#CBD5E1",
        "text": "#0F172A",
        "text_muted": "#64748B",
        "btn_hover": "rgba(0, 0, 0, 0.06)",
        "accent": "#2563EB",
        "accent_bg": "rgba(37, 99, 235, 0.15)",
        "success": "#10B981",
        "danger": "#EF4444",
        "banner_bg": "#EEF2FF",
        "banner_text": "#3730A3",
        "table_border": "#CBD5E1",
        "table_header_bg": "#F1F5F9",
        "table_alt_bg": "#F8FAFC",
        "scrollbar": "#CBD5E1",
    }
}


def convert_markdown_tables(text: str) -> str:
    """Detects markdown tables in text and converts them to styled HTML tables."""
    lines = text.split("\n")
    result = []
    i = 0
    found_table = False
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith("|") and re.search(r"\|?\s*:?-+:?\s*\|", next_line):
                found_table = True
                headers = [html.escape(c.strip()) for c in line.strip("|").split("|")]
                table_html = [
                    '<table border="1" cellpadding="6" cellspacing="0" '
                    'style="border-collapse:collapse; width:100%; margin:8px 0;">'
                ]
                table_html.append(
                    '<thead><tr style="background-color:#333; color:#fff;">'
                    + ''.join(f'<th style="font-weight:bold; padding:6px 10px; border:1px solid #555;">{h}</th>' for h in headers)
                    + '</tr></thead><tbody>'
                )
                i += 2
                row_idx = 0
                while i < len(lines) and lines[i].strip().startswith("|"):
                    row_cells = [html.escape(c.strip()) for c in lines[i].strip("|").split("|")]
                    bg_style = ' style="background-color:#2a2a2a;"' if row_idx % 2 == 1 else ''
                    table_html.append(
                        f'<tr{bg_style}>'
                        + ''.join(f'<td style="padding:6px 10px; border:1px solid #555;">{c}</td>' for c in row_cells)
                        + '</tr>'
                    )
                    row_idx += 1
                    i += 1
                table_html.append('</tbody></table><p></p>')
                result.append("".join(table_html))
                continue
        result.append(html.escape(lines[i]))
        i += 1

    if found_table:
        return "<br/>".join(result)
    return ""


class RichTextEditor(QTextEdit):
    """Rich text editor with native support for pasted screenshots, draggable corner resize handles, and tables."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setAcceptRichText(True)
        self.setTabChangesFocus(False)

        # Image selection & resize state
        self.selected_image_pos = -1
        self.active_handle = None
        self.drag_start_pos = None
        self.drag_start_rect = None
        self.current_drag_rect = None

        # Viewport monitoring for handle rendering & interaction
        self.viewport().installEventFilter(self)
        self.viewport().setMouseTracking(True)
        self.verticalScrollBar().valueChanged.connect(self.viewport().update)
        self.horizontalScrollBar().valueChanged.connect(self.viewport().update)
        self.textChanged.connect(self._on_editor_text_changed)

    def paintEvent(self, event):
        """Paint document content normally, then overlay selection handles on top if an image is selected."""
        super().paintEvent(event)
        self.paint_handles()

    def _on_editor_text_changed(self):
        """Validate currently selected image position when document text changes."""
        if self.selected_image_pos != -1:
            if not self.get_selected_image_rect():
                self.selected_image_pos = -1
                self.viewport().update()

    def find_image_at_pos(self, pt: QPoint):
        """Find if a viewport position falls inside any rendered image."""
        doc = self.document()
        block = doc.begin()
        while block.isValid():
            it = block.begin()
            while not it.atEnd():
                frag = it.fragment()
                if frag.isValid() and frag.charFormat().isImageFormat():
                    fmt = frag.charFormat().toImageFormat()
                    c = self.textCursor()
                    c.setPosition(frag.position())
                    cr = self.cursorRect(c)
                    res = doc.resource(QTextDocument.ResourceType.ImageResource, QUrl(fmt.name()))
                    res_w = res.width() if res and not res.isNull() else 100
                    res_h = res.height() if res and not res.isNull() else cr.height()
                    w = int(fmt.width()) if fmt.width() > 0 else res_w
                    h = int(fmt.height()) if fmt.height() > 0 else (int(cr.height()) if cr.height() > 0 else res_h)
                    img_rect = QRect(cr.x(), cr.y(), w, h)
                    if img_rect.contains(pt):
                        return frag.position(), img_rect, fmt
                it += 1
            block = block.next()
        return -1, None, None

    def get_selected_image_rect(self):
        """Compute current viewport rectangle for the selected image."""
        if self.selected_image_pos == -1:
            return None
        c = self.textCursor()
        c.setPosition(self.selected_image_pos)
        c.setPosition(self.selected_image_pos + 1, QTextCursor.MoveMode.KeepAnchor)
        fmt = c.charFormat()
        if not fmt.isImageFormat():
            return None
        img_fmt = fmt.toImageFormat()
        c.setPosition(self.selected_image_pos)
        cr = self.cursorRect(c)
        res = self.document().resource(QTextDocument.ResourceType.ImageResource, QUrl(img_fmt.name()))
        res_w = res.width() if res and not res.isNull() else 100
        res_h = res.height() if res and not res.isNull() else cr.height()
        w = int(img_fmt.width()) if img_fmt.width() > 0 else res_w
        h = int(img_fmt.height()) if img_fmt.height() > 0 else (int(cr.height()) if cr.height() > 0 else res_h)
        return QRect(cr.x(), cr.y(), w, h)

    def get_handles(self, rect: QRect):
        """Get 4 corner resize handles (top-left, top-right, bottom-left, bottom-right)."""
        hs = 9
        half = hs // 2
        return {
            "tl": QRect(rect.left() - half, rect.top() - half, hs, hs),
            "tr": QRect(rect.right() - half, rect.top() - half, hs, hs),
            "bl": QRect(rect.left() - half, rect.bottom() - half, hs, hs),
            "br": QRect(rect.right() - half, rect.bottom() - half, hs, hs),
        }

    def keyPressEvent(self, event):
        """Delete selected image when Delete or Backspace is pressed."""
        if self.selected_image_pos != -1 and event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
            c = self.textCursor()
            c.setPosition(self.selected_image_pos)
            c.setPosition(self.selected_image_pos + 1, QTextCursor.MoveMode.KeepAnchor)
            c.removeSelectedText()
            self.selected_image_pos = -1
            self.viewport().update()
            if hasattr(self, "parent_app") and self.parent_app:
                self.parent_app.save_now()
            return
        super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.viewport():
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    pt = event.pos()
                    # 1. Check if clicked on a corner handle of already selected image
                    img_rect = self.get_selected_image_rect()
                    if img_rect:
                        handles = self.get_handles(img_rect)
                        for h_id, h_rect in handles.items():
                            if h_rect.adjusted(-3, -3, 3, 3).contains(pt):
                                self.active_handle = h_id
                                self.drag_start_pos = pt
                                self.drag_start_rect = img_rect
                                self.current_drag_rect = img_rect
                                return True

                    # 2. Check if clicked on any image in document
                    pos, rect, fmt = self.find_image_at_pos(pt)
                    if pos != -1:
                        self.selected_image_pos = pos
                        self.viewport().update()
                        return True
                    else:
                        if self.selected_image_pos != -1:
                            self.selected_image_pos = -1
                            self.viewport().update()

            elif event.type() == QEvent.Type.MouseMove:
                pt = event.pos()
                if self.active_handle and self.drag_start_rect:
                    orig = self.drag_start_rect
                    aspect = orig.width() / max(1, orig.height())
                    max_w = max(80, self.viewport().width() - 24)

                    if self.active_handle in ("br", "tr"):
                        dx = pt.x() - self.drag_start_pos.x()
                        new_w = max(40, min(max_w, orig.width() + dx))
                    else:
                        dx = self.drag_start_pos.x() - pt.x()
                        new_w = max(40, min(max_w, orig.width() + dx))

                    new_h = max(20, int(new_w / aspect))

                    if self.active_handle == "br":
                        self.current_drag_rect = QRect(orig.left(), orig.top(), new_w, new_h)
                    elif self.active_handle == "bl":
                        self.current_drag_rect = QRect(orig.right() - new_w, orig.top(), new_w, new_h)
                    elif self.active_handle == "tr":
                        self.current_drag_rect = QRect(orig.left(), orig.bottom() - new_h, new_w, new_h)
                    elif self.active_handle == "tl":
                        self.current_drag_rect = QRect(orig.right() - new_w, orig.bottom() - new_h, new_w, new_h)

                    self.viewport().update()
                    return True
                else:
                    # Update hover cursor over handles
                    img_rect = self.get_selected_image_rect()
                    if img_rect:
                        handles = self.get_handles(img_rect)
                        for h_id, h_rect in handles.items():
                            if h_rect.adjusted(-3, -3, 3, 3).contains(pt):
                                if h_id in ("tl", "br"):
                                    self.viewport().setCursor(Qt.CursorShape.SizeFDiagCursor)
                                else:
                                    self.viewport().setCursor(Qt.CursorShape.SizeBDiagCursor)
                                return True
                    self.viewport().setCursor(Qt.CursorShape.IBeamCursor)

            elif event.type() == QEvent.Type.MouseButtonRelease:
                if self.active_handle and self.current_drag_rect:
                    new_w = self.current_drag_rect.width()
                    new_h = self.current_drag_rect.height()

                    c = self.textCursor()
                    c.setPosition(self.selected_image_pos)
                    c.setPosition(self.selected_image_pos + 1, QTextCursor.MoveMode.KeepAnchor)
                    fmt = c.charFormat().toImageFormat()
                    fmt.setWidth(new_w)
                    fmt.setHeight(new_h)
                    c.setCharFormat(fmt)

                    self.active_handle = None
                    self.drag_start_pos = None
                    self.drag_start_rect = None
                    self.current_drag_rect = None
                    self.viewport().update()

                    if hasattr(self, "parent_app") and self.parent_app:
                        self.parent_app.save_now()
                    return True

        return super().eventFilter(obj, event)

    def paint_handles(self):
        """Draw MS Office-style bounding box and 4 corner pointers around selected image."""
        rect = self.current_drag_rect or self.get_selected_image_rect()
        if not rect:
            return

        p = QPainter(self.viewport())
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw selection border
        pen = QPen(QColor("#2563EB"), 1.5, Qt.PenStyle.DashLine if self.active_handle else Qt.PenStyle.SolidLine)
        p.setPen(pen)
        p.setBrush(QColor(37, 99, 235, 18) if self.active_handle else Qt.BrushStyle.NoBrush)
        p.drawRect(rect)

        # Draw 4 corner handles (pointers)
        handles = self.get_handles(rect)
        handle_pen = QPen(QColor("#2563EB"), 1.5)
        handle_brush = QBrush(QColor("#FFFFFF"))
        p.setPen(handle_pen)
        p.setBrush(handle_brush)
        for h_rect in handles.values():
            p.drawRoundedRect(h_rect, 2, 2)

        # Dimension tooltip badge while dragging
        if self.active_handle and self.current_drag_rect:
            dim_text = f"{self.current_drag_rect.width()} × {self.current_drag_rect.height()}"
            p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            badge_rect = QRect(rect.center().x() - 36, rect.bottom() + 8, 72, 20)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(24, 24, 27, 220))
            p.drawRoundedRect(badge_rect, 4, 4)
            p.setPen(QColor("#FFFFFF"))
            p.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, dim_text)

        p.end()

    def set_selected_image_size(self, width: int, height: int = 0):
        """Programmatically set selected image dimensions."""
        if self.selected_image_pos == -1:
            return
        c = self.textCursor()
        c.setPosition(self.selected_image_pos)
        c.setPosition(self.selected_image_pos + 1, QTextCursor.MoveMode.KeepAnchor)
        fmt = c.charFormat()
        if fmt.isImageFormat():
            img_fmt = fmt.toImageFormat()
            orig_w = img_fmt.width() if img_fmt.width() > 0 else 100
            orig_h = img_fmt.height() if img_fmt.height() > 0 else 100
            aspect = orig_w / max(1, orig_h)
            if height <= 0:
                height = int(width / aspect)
            img_fmt.setWidth(width)
            img_fmt.setHeight(height)
            c.setCharFormat(img_fmt)
            self.viewport().update()
            if hasattr(self, "parent_app") and self.parent_app:
                self.parent_app.save_now()

    def canInsertFromMimeData(self, source):
        """Allow inserting images, screenshots, and image file paths directly."""
        if source.hasImage() or source.hasUrls():
            return True
        return super().canInsertFromMimeData(source)

    def insert_image(self, img: QImage):
        """Insert a QImage as a responsive, base64-encoded PNG inline."""
        if img.isNull():
            return
        # If image is excessively wide (e.g. 4K retina screenshot), scale down smoothly
        if img.width() > 1400:
            img = img.scaledToWidth(1400, Qt.TransformationMode.SmoothTransformation)

        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODevice.OpenModeFlag.WriteOnly)
        img.save(buf, "PNG")
        b64 = base64.b64encode(ba.data()).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64}"

        # Determine fitting display width for the sticky note
        viewport_w = self.viewport().width()
        display_w = max(180, viewport_w - 24) if viewport_w > 50 else 320
        aspect = img.width() / max(1, img.height())
        display_h = max(20, int(display_w / aspect))

        cursor = self.textCursor()
        cursor.insertHtml(f'<p><img src="{data_uri}" width="{display_w}" height="{display_h}"/></p><p><br/></p>')
        self.ensureCursorVisible()

    def insertFromMimeData(self, source):
        """Handle rich paste: screenshots, copied pictures, tables from Gemini/Word/Web, or Markdown tables."""
        # 1. Direct Image in clipboard (e.g. Snipping tool, Win+Shift+S, PrintScreen, copied picture)
        if source.hasImage():
            img_data = source.imageData()
            if isinstance(img_data, QPixmap):
                img_data = img_data.toImage()
            if isinstance(img_data, QImage) and not img_data.isNull():
                self.insert_image(img_data)
                return

        # 2. Copied image files (e.g. copied from Windows Explorer / macOS Finder)
        if source.hasUrls():
            img_urls = []
            for u in source.urls():
                lp = u.toLocalFile()
                if lp and lp.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    img_urls.append(lp)
            if img_urls:
                for path in img_urls:
                    img = QImage(path)
                    if not img.isNull():
                        self.insert_image(img)
                return

        # 3. HTML with tables
        if source.hasHtml():
            raw_html = source.html()
            if "<table" in raw_html.lower():
                styled_html = re.sub(
                    r'<table(?![^>]*\bborder=)',
                    r'<table border="1" style="border-collapse:collapse; width:100%; margin:8px 0;"',
                    raw_html,
                    flags=re.IGNORECASE
                )
                self.textCursor().insertHtml(styled_html)
                return
            super().insertFromMimeData(source)
            return

        # 4. Markdown tables
        if source.hasText():
            plain = source.text()
            if "|" in plain and "\n" in plain:
                converted_html = convert_markdown_tables(plain)
                if converted_html:
                    self.textCursor().insertHtml(converted_html)
                    return

        super().insertFromMimeData(source)


class TableDialog(QDialog):
    """Dialog to insert a table into the note."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Table")
        self.setFixedSize(240, 150)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QFormLayout(self)
        self.rows_spin = QSpinBox(self)
        self.rows_spin.setRange(1, 20)
        self.rows_spin.setValue(3)

        self.cols_spin = QSpinBox(self)
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(3)

        layout.addRow("Rows:", self.rows_spin)
        layout.addRow("Columns:", self.cols_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_dimensions(self):
        return self.rows_spin.value(), self.cols_spin.value()


class DraggableTitleBar(QFrame):
    """Custom title bar supporting smooth window dragging and double-click maximize."""
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.win = parent_window

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.win.drag_pos = event.globalPosition().toPoint() - self.win.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and getattr(self.win, "drag_pos", None) is not None:
            self.win.move(event.globalPosition().toPoint() - self.win.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.win.drag_pos = None
        self.win.save_now()
        event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.win.toggle_maximize()
            event.accept()


class PinNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load persisted settings
        self.settings = load_data()
        self.is_pinned = bool(self.settings.get("always_on_top", True))
        self.theme = self.settings.get("theme", "dark")
        if self.theme not in THEMES:
            self.theme = "dark"
        self.font_size = int(self.settings.get("font_size", 13))
        self.start_on_boot = is_start_on_boot_enabled()
        self.last_cleared_html = ""

        # Dragging state
        self.drag_pos = None

        # Debounced auto-save timer
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.setInterval(350)
        self.save_timer.timeout.connect(self.save_now)

        # Toast banner timer
        self.toast_timer = QTimer(self)
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self.hide_toast)

        # Inactivity auto-transparency settings
        self.idle_enabled = bool(self.settings.get("idle_transparency_enabled", True))
        self.idle_timeout_seconds = int(self.settings.get("idle_timeout_seconds", 60))
        self.idle_opacity = int(self.settings.get("idle_opacity", 50))
        self.is_dimmed = False

        # Inactivity countdown timer
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.setSingleShot(True)
        self.inactivity_timer.timeout.connect(self._on_inactivity_timeout)

        # Opacity transition animation
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(280)

        # Global event filter to detect activity
        QApplication.instance().installEventFilter(self)

        # Setup modern frameless window with min/max taskbar buttons
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowSystemMenuHint |
            Qt.WindowType.WindowMinMaxButtonsHint
        )
        self.setMinimumSize(300, 240)

        # Restore Always-on-Top initially
        if self.is_pinned:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        # Build UI layout
        self._build_ui()
        self._apply_theme()
        self._restore_content()
        self._restore_geometry_safely()
        self._setup_shortcuts()

        # Start idle countdown if enabled
        if self.idle_enabled:
            self.inactivity_timer.start(self.idle_timeout_seconds * 1000)

    def _build_ui(self):
        """Construct the modern frameless UI layout."""
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(0)

        # 1. Custom Title Bar
        self._create_title_bar()

        # 2. Notification / Undo Banner
        self._create_toast_banner()

        # 3. Rich Text Editor
        self.editor = RichTextEditor(self)
        self.editor.setFont(get_app_font(self.font_size))
        self.editor.textChanged.connect(self._on_content_changed)
        self.editor.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self._show_context_menu)
        self.main_layout.addWidget(self.editor)

        # 4. Footer Bar
        self._create_footer()

        self.setCentralWidget(self.central_widget)

        # Enable mouse tracking so cursor movements are detected without mouse press
        self.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)
        self.title_bar.setMouseTracking(True)
        self.footer.setMouseTracking(True)

    def _create_title_bar(self):
        """Minimalist compact title bar with line vector icons."""
        self.title_bar = DraggableTitleBar(self)
        self.title_bar.setFixedHeight(34)
        self.title_bar.setObjectName("title_bar")

        tb_layout = QHBoxLayout(self.title_bar)
        tb_layout.setContentsMargins(10, 0, 4, 0)
        tb_layout.setSpacing(2)

        # Left: App Icon, Title and Save Status
        self.app_icon = QLabel(self.title_bar)
        self.app_icon.setFixedSize(16, 16)
        icon_png = get_asset_path("icon.png")
        if os.path.exists(icon_png):
            self.app_icon.setPixmap(
                QPixmap(icon_png).scaled(
                    16, 16,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        self.app_icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.title_label = QLabel("PinNote", self.title_bar)
        self.title_label.setFont(get_app_font(10, bold=True))
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.status_label = QLabel("● Saved", self.title_bar)
        self.status_label.setFont(get_app_font(8))
        self.status_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        tb_layout.addWidget(self.app_icon)
        tb_layout.addSpacing(4)
        tb_layout.addWidget(self.title_label)
        tb_layout.addSpacing(6)
        tb_layout.addWidget(self.status_label)
        tb_layout.addStretch()

        # Center/Right: Action Buttons (Minimal borderless ghost buttons)
        self.copy_btn = QPushButton(self.title_bar)
        self.copy_btn.setFixedSize(24, 24)
        self.copy_btn.setToolTip("Copy Note")
        self.copy_btn.clicked.connect(self.copy_all_text)
        self.copy_btn.setProperty("class", "ghost_btn")

        self.clear_btn = QPushButton(self.title_bar)
        self.clear_btn.setFixedSize(24, 24)
        self.clear_btn.setToolTip("Clear Note")
        self.clear_btn.clicked.connect(self.clear_all_text)
        self.clear_btn.setProperty("class", "ghost_btn")

        self.theme_btn = QPushButton(self.title_bar)
        self.theme_btn.setFixedSize(24, 24)
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setProperty("class", "ghost_btn")

        tb_layout.addWidget(self.copy_btn)
        tb_layout.addWidget(self.clear_btn)
        tb_layout.addWidget(self.theme_btn)
        tb_layout.addSpacing(4)

        # Window Controls Cluster: [ 📌 Pin ] [ — Min ] [ □ Max ] [ ✕ Close ]
        self.pin_btn = QPushButton(self.title_bar)
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.clicked.connect(self.toggle_always_on_top)
        self.pin_btn.setProperty("class", "ghost_btn")

        self.min_btn = QPushButton(self.title_bar)
        self.min_btn.setFixedSize(26, 26)
        self.min_btn.setToolTip("Minimize")
        self.min_btn.clicked.connect(self.showMinimized)
        self.min_btn.setProperty("class", "ghost_btn")

        self.max_btn = QPushButton(self.title_bar)
        self.max_btn.setFixedSize(26, 26)
        self.max_btn.setToolTip("Maximize / Restore")
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.max_btn.setProperty("class", "ghost_btn")

        self.close_btn = QPushButton(self.title_bar)
        self.close_btn.setFixedSize(26, 26)
        self.close_btn.setToolTip("Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setProperty("class", "close_btn")

        tb_layout.addWidget(self.pin_btn)
        tb_layout.addWidget(self.min_btn)
        tb_layout.addWidget(self.max_btn)
        tb_layout.addWidget(self.close_btn)

        self.main_layout.addWidget(self.title_bar)

    def _create_toast_banner(self):
        """Notification banner for Undo and actions."""
        self.toast_banner = QFrame(self)
        self.toast_banner.setFixedHeight(30)
        self.toast_banner.setObjectName("toast_banner")
        b_layout = QHBoxLayout(self.toast_banner)
        b_layout.setContentsMargins(10, 0, 10, 0)
        b_layout.setSpacing(6)

        self.toast_label = QLabel("", self.toast_banner)
        self.toast_label.setFont(get_app_font(9))
        self.toast_label.setObjectName("toast_label")
        b_layout.addWidget(self.toast_label)
        b_layout.addStretch()

        self.undo_btn = QPushButton("↺ Undo", self.toast_banner)
        self.undo_btn.setFixedSize(54, 22)
        self.undo_btn.setFont(get_app_font(8, bold=True))
        self.undo_btn.clicked.connect(self.undo_clear)
        b_layout.addWidget(self.undo_btn)

        self.toast_banner.hide()
        self.main_layout.addWidget(self.toast_banner)

    def _create_footer(self):
        """Footer bar with live counts, font controls, boot switch, and resize grip."""
        self.footer = QFrame(self)
        self.footer.setFixedHeight(28)
        self.footer.setObjectName("footer")
        f_layout = QHBoxLayout(self.footer)
        f_layout.setContentsMargins(10, 0, 0, 0)
        f_layout.setSpacing(6)

        # Word & Char counts
        self.counter_label = QLabel("0 words • 0 chars", self.footer)
        self.counter_label.setFont(get_app_font(8))
        f_layout.addWidget(self.counter_label)
        f_layout.addStretch()

        # Font size adjusters
        self.font_dec_btn = QPushButton("A-", self.footer)
        self.font_dec_btn.setFixedSize(24, 20)
        self.font_dec_btn.setFont(get_app_font(8))
        self.font_dec_btn.setToolTip(f"Decrease Font Size ({MOD_KEY}+-)")
        self.font_dec_btn.clicked.connect(self.decrease_font_size)
        f_layout.addWidget(self.font_dec_btn)

        self.font_size_label = QLabel(f"{self.font_size}pt", self.footer)
        self.font_size_label.setFont(get_app_font(8))
        self.font_size_label.setObjectName("font_size_label")
        f_layout.addWidget(self.font_size_label)

        self.font_inc_btn = QPushButton("A+", self.footer)
        self.font_inc_btn.setFixedSize(24, 20)
        self.font_inc_btn.setFont(get_app_font(8))
        self.font_inc_btn.setToolTip(f"Increase Font Size ({MOD_KEY}++)")
        self.font_inc_btn.clicked.connect(self.increase_font_size)
        f_layout.addWidget(self.font_inc_btn)

        # Settings button (opens settings menu with boot and idle transparency options)
        self.settings_btn = QPushButton(self.footer)
        self.settings_btn.setFixedSize(24, 20)
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        self.settings_btn.setProperty("class", "ghost_btn")
        f_layout.addWidget(self.settings_btn)

        # Native corner resize grip
        self.size_grip = QSizeGrip(self)
        f_layout.addWidget(self.size_grip)

        self.main_layout.addWidget(self.footer)

    def _setup_shortcuts(self):
        """Keyboard shortcuts."""
        QShortcut(QKeySequence("Ctrl+P"), self, self.toggle_always_on_top)
        QShortcut(QKeySequence("Ctrl+S"), self, lambda: self.save_now(show_feedback=True))
        QShortcut(QKeySequence("Ctrl+B"), self, self.toggle_bold)
        QShortcut(QKeySequence("Ctrl+I"), self, self.toggle_italic)
        QShortcut(QKeySequence("Ctrl+U"), self, self.toggle_underline)
        QShortcut(QKeySequence("Ctrl+="), self, self.increase_font_size)
        QShortcut(QKeySequence("Ctrl++"), self, self.increase_font_size)
        QShortcut(QKeySequence("Ctrl+-"), self, self.decrease_font_size)
        QShortcut(QKeySequence(f"{MOD_KEY}+Shift+C"), self, self.copy_note_as_screenshot)

    def _apply_theme(self):
        """Apply active theme styles and render minimalist vector SVG icons."""
        t = THEMES[self.theme]
        icon_color = t["text_muted"]

        # Render vector SVG icons
        self.copy_btn.setIcon(render_svg_icon("copy", icon_color, size=13))
        self.clear_btn.setIcon(render_svg_icon("trash", icon_color, size=13))

        theme_icon_name = "sun" if self.theme == "dark" else "moon"
        self.theme_btn.setIcon(render_svg_icon(theme_icon_name, icon_color, size=13))
        self.theme_btn.setToolTip(f"Switch to {'Light' if self.theme == 'dark' else 'Dark'} Mode")

        self.min_btn.setIcon(render_svg_icon("minimize", icon_color, size=12))
        max_icon_name = "restore" if self.isMaximized() else "maximize"
        self.max_btn.setIcon(render_svg_icon(max_icon_name, icon_color, size=12))
        self.close_btn.setIcon(render_svg_icon("close", icon_color, size=12))
        self.settings_btn.setIcon(render_svg_icon("settings", icon_color, size=13))

        self._update_pin_button_style()

        check_icon_path = get_asset_path("checkmark.svg").replace("\\", "/")

        qss = f"""
        QMainWindow {{
            background-color: {t['bg']};
        }}
        QWidget#central_widget {{
            background-color: {t['bg']};
            border: 1px solid {t['border']};
            border-radius: 8px;
        }}
        QFrame#title_bar {{
            background-color: {t['title_bg']};
            border: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }}
        QFrame#footer {{
            background-color: {t['title_bg']};
            border: none;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }}
        QLabel {{
            color: {t['text']};
        }}
        QTextEdit {{
            background-color: {t['card_bg']};
            color: {t['text']};
            border: 1px solid {t['border']};
            border-radius: 6px;
            padding: 8px;
            selection-background-color: {t['accent']};
            selection-color: #FFFFFF;
        }}
        QTextEdit table {{
            border: 1px solid {t['table_border']};
            border-collapse: collapse;
        }}
        QTextEdit th {{
            background-color: {t['table_header_bg']};
            color: {t['text']};
            border: 1px solid {t['table_border']};
            font-weight: bold;
            padding: 6px 10px;
        }}
        QTextEdit td {{
            border: 1px solid {t['table_border']};
            padding: 6px 10px;
        }}
        QScrollBar:vertical {{
            background: {t['card_bg']};
            width: 8px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {t['scrollbar']};
            min-height: 20px;
            border-radius: 4px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        /* Minimalist Ghost Buttons */
        QPushButton[class="ghost_btn"] {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 2px;
        }}
        QPushButton[class="ghost_btn"]:hover {{
            background-color: {t['btn_hover']};
        }}
        QPushButton[class="close_btn"] {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 2px;
        }}
        QPushButton[class="close_btn"]:hover {{
            background-color: {t['danger']};
        }}
        /* Footer font buttons */
        QFrame#footer QPushButton {{
            background-color: {t['btn_hover']};
            color: {t['text_muted']};
            border: none;
            border-radius: 3px;
        }}
        QFrame#footer QPushButton:hover {{
            color: {t['text']};
        }}
        QLabel#font_size_label {{
            color: {t['text_muted']};
            padding: 0 3px;
        }}
        /* Toast banner */
        QFrame#toast_banner {{
            background-color: {t['banner_bg']};
            border-radius: 4px;
        }}
        QLabel#toast_label {{
            color: {t['banner_text']};
        }}
        /* Checkbox with sleek checkmark tick */
        QCheckBox {{
            color: {t['text_muted']};
            spacing: 6px;
        }}
        QCheckBox::indicator {{
            width: 13px;
            height: 13px;
            border: 1px solid {t['border']};
            border-radius: 3px;
            background-color: transparent;
        }}
        QCheckBox::indicator:hover {{
            border-color: {t['accent']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {t['accent']};
            border: 1px solid {t['accent']};
            image: url({check_icon_path});
        }}
        /* Settings Dialog, ComboBox and Slider */
        QDialog {{
            background-color: {t['bg']};
            color: {t['text']};
        }}
        QComboBox {{
            background-color: {t['card_bg']};
            color: {t['text']};
            border: 1px solid {t['border']};
            border-radius: 4px;
            padding: 4px 8px;
        }}
        QComboBox::drop-down {{
            border: none;
            width: 18px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {t['card_bg']};
            color: {t['text']};
            selection-background-color: {t['accent']};
            selection-color: #FFFFFF;
            border: 1px solid {t['border']};
        }}
        QSlider::groove:horizontal {{
            height: 4px;
            background: {t['scrollbar']};
            border-radius: 2px;
        }}
        QSlider::sub-page:horizontal {{
            background: {t['accent']};
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background: #FFFFFF;
            border: 1px solid {t['accent']};
            width: 14px;
            margin-top: -5px;
            margin-bottom: -5px;
            border-radius: 7px;
        }}
        /* Modern Popup Settings Menu */
        QMenu {{
            background-color: {t['card_bg']};
            color: {t['text']};
            border: 1px solid {t['border']};
            border-radius: 8px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 6px 20px 6px 24px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {t['btn_hover']};
            color: {t['text']};
        }}
        QMenu::item:disabled {{
            color: {t['text_muted']};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: {t['border']};
            margin: 4px 6px;
        }}
        QMenu::indicator {{
            width: 13px;
            height: 13px;
            left: 6px;
        }}
        QMenu::indicator:checked {{
            image: url({check_icon_path});
        }}
        """
        self.setStyleSheet(qss)

    def _update_pin_button_style(self):
        t = THEMES[self.theme]
        if self.is_pinned:
            # Active state: blue vector pin with subtle tinted background
            self.pin_btn.setIcon(render_svg_icon("pin_active", t["accent"], size=13))
            self.pin_btn.setStyleSheet(
                f"background-color: {t['accent_bg']}; border-radius: 4px; border: none;"
            )
            self.pin_btn.setToolTip("Always on Top: ON (Click to unpin)")
        else:
            # Inactive state: subtle neutral monochrome vector pin
            self.pin_btn.setIcon(render_svg_icon("pin", t["text_muted"], size=13))
            self.pin_btn.setStyleSheet(
                f"background-color: transparent; border-radius: 4px; border: none;"
            )
            self.pin_btn.setToolTip("Always on Top: OFF (Click to pin)")

    def _restore_content(self):
        """Restore saved note content."""
        saved_html = self.settings.get("html", "")
        saved_text = self.settings.get("text", "")
        if saved_html:
            self.editor.setHtml(saved_html)
        elif saved_text:
            escaped = html.escape(saved_text).replace("\n", "<br/>")
            self.editor.setHtml(f"<p>{escaped}</p>")
        else:
            starter = """<h3>Welcome to PinNote! 📌</h3>
<p>You can type, paste rich text, or paste tables here from <b>Gemini</b>, <b>Word</b>, or <b>Excel</b>!</p>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%; margin:8px 0;">
  <thead>
    <tr>
      <th style="font-weight:bold; padding:6px 10px;">Feature</th>
      <th style="font-weight:bold; padding:6px 10px;">Status</th>
      <th style="font-weight:bold; padding:6px 10px;">Shortcut</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:6px 10px;">Always-on-Top</td>
      <td style="padding:6px 10px;">Active</td>
      <td style="padding:6px 10px;">Ctrl + P</td>
    </tr>
    <tr>
      <td style="padding:6px 10px;">Reboot Auto-Save</td>
      <td style="padding:6px 10px;">Continuous</td>
      <td style="padding:6px 10px;">Ctrl + S</td>
    </tr>
    <tr>
      <td style="padding:6px 10px;">Theme Switch</td>
      <td style="padding:6px 10px;">Dark / Light</td>
      <td style="padding:6px 10px;">Sun / Moon button</td>
    </tr>
  </tbody>
</table>
<p><i>Edit or remove this text anytime.</i></p>"""
            self.editor.setHtml(starter)

        # Apply font size across all loaded text and tables
        self._apply_font_size_to_document(self.font_size)

        self._update_counts()

    def _restore_geometry_safely(self):
        """Ensure window coordinates are visible and inside user's active screen."""
        primary = QApplication.primaryScreen().availableGeometry()
        default_w = 380
        default_h = 500
        default_x = max(60, primary.width() - default_w - 60)
        default_y = max(60, primary.top() + 80)

        saved_geom = self.settings.get("geometry", "")
        if saved_geom and "+" in saved_geom:
            try:
                dims, pos = saved_geom.split("+", 1)
                w, h = map(int, dims.split("x"))
                x, y = map(int, pos.split("+"))

                w = max(300, min(w, primary.width()))
                h = max(240, min(h, primary.height()))

                rect = QRect(x, y, w, h)
                is_on_screen = False
                for screen in QApplication.screens():
                    avail = screen.availableGeometry()
                    inter = avail.intersected(rect)
                    if inter.width() >= 120 and inter.height() >= 120:
                        is_on_screen = True
                        break

                if is_on_screen:
                    self.setGeometry(x, y, w, h)
                    return
            except Exception:
                pass

        self.setGeometry(default_x, default_y, default_w, default_h)

    def _on_content_changed(self):
        """Debounced auto-save on typing."""
        t = THEMES[self.theme]
        self.status_label.setText("● Saving...")
        self.status_label.setStyleSheet(f"color: {t['text_muted']};")
        self._update_counts()
        self.save_timer.start()

    def _update_counts(self):
        """Update live word and char count."""
        plain = self.editor.toPlainText().strip()
        chars = len(plain)
        words = len(plain.split()) if plain else 0
        self.counter_label.setText(f"{words} words • {chars} chars")

    def toggle_always_on_top(self):
        """Toggle Always-on-Top mode without losing window position."""
        self.is_pinned = not self.is_pinned
        geo = self.geometry()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.is_pinned)
        self.setGeometry(geo)
        self.show()
        self.raise_()
        self.activateWindow()
        self._update_pin_button_style()
        self.show_toast(
            "📌 Window set to Always-on-Top" if self.is_pinned else "Window unpinned (normal mode)",
            duration=1800
        )
        self.save_now()

    def toggle_theme(self):
        """Toggle Dark Mode / Light Mode."""
        self.theme = "light" if self.theme == "dark" else "dark"
        self._apply_theme()
        self.show_toast(f"Switched to {'Light' if self.theme == 'light' else 'Dark'} Mode", duration=1500)
        self.save_now()

    def toggle_maximize(self):
        """Toggle maximize / restore."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        t = THEMES[self.theme]
        max_icon_name = "restore" if self.isMaximized() else "maximize"
        self.max_btn.setIcon(render_svg_icon(max_icon_name, t["text_muted"], size=12))

    def toggle_start_on_boot(self, checked):
        """Toggle Windows Startup."""
        success = set_start_on_boot(checked)
        if success:
            self.start_on_boot = checked
            msg = "✓ PinNote will open on Windows reboot" if checked else "PinNote removed from Windows startup"
            self.show_toast(msg, duration=2200)
            self.save_now()
        else:
            self.show_toast("⚠️ Failed to update startup", duration=2500)

    def _extract_first_image_from_html(self, html_str: str):
        """Extract first embedded base64 image from HTML if present."""
        match = re.search(r'<img[^>]+src=["\']data:image/[^;]+;base64,([^"\']+)["\']', html_str, re.IGNORECASE)
        if match:
            try:
                b64_data = match.group(1)
                raw_bytes = base64.b64decode(b64_data)
                img = QImage()
                if img.loadFromData(raw_bytes):
                    return img
            except Exception:
                pass
        return None

    def copy_all_text(self):
        """Copy note to clipboard (providing plain text, formatted HTML, and image data)."""
        html_content = self.editor.toHtml()
        plain_text = self.editor.toPlainText().strip()

        cb = QApplication.clipboard()
        mime = QMimeData()
        mime.setText(self.editor.toPlainText())
        mime.setHtml(html_content)

        # If note contains an embedded screenshot / image, attach it as clipboard image too!
        extracted_img = self._extract_first_image_from_html(html_content)
        if extracted_img:
            mime.setImageData(extracted_img)

        cb.setMimeData(mime)
        self.show_toast("📋 Note copied to clipboard!", duration=1500)

    def copy_note_as_screenshot(self):
        """Capture the visual note card as a high-resolution screenshot image to clipboard."""
        QApplication.processEvents()
        pixmap = self.central_widget.grab()
        if not pixmap.isNull():
            cb = QApplication.clipboard()
            cb.setImage(pixmap.toImage())
            self.show_toast("📸 Note screenshot copied!", duration=1800)

    def clear_all_text(self):
        """Clear note with instant 6-second Undo option."""
        html_content = self.editor.toHtml()
        if not self.editor.toPlainText().strip():
            return
        self.last_cleared_html = html_content
        self.editor.clear()
        self.save_now()
        self.show_toast("Note cleared", show_undo=True, duration=6000)

    def undo_clear(self):
        """Restore cleared note."""
        if self.last_cleared_html:
            self.editor.setHtml(self.last_cleared_html)
            self.last_cleared_html = ""
            self.hide_toast()
            self.save_now()
            self.show_toast("↺ Note restored!", duration=1500)

    def _apply_font_size_to_document(self, new_size):
        """Robustly applies font size across all existing text, blocks, tables, and future typing."""
        doc = self.editor.document()

        # Update default font & editor properties
        dfont = doc.defaultFont()
        dfont.setPointSize(new_size)
        doc.setDefaultFont(dfont)
        self.editor.setFont(get_app_font(new_size))
        self.editor.setFontPointSize(new_size)

        cursor = self.editor.textCursor()
        orig_pos = cursor.position()
        orig_anchor = cursor.anchor()

        cursor.beginEditBlock()
        fmt = QTextCharFormat()
        fmt.setFontPointSize(new_size)

        # 1. Document-wide selection merge
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeCharFormat(fmt)

        # 2. Iterate every block and fragment to guarantee tables and spans update
        block = doc.begin()
        while block.isValid():
            it = block.begin()
            while not it.atEnd():
                fragment = it.fragment()
                if fragment.isValid():
                    c = QTextCursor(doc)
                    c.setPosition(fragment.position())
                    c.setPosition(fragment.position() + fragment.length(), QTextCursor.MoveMode.KeepAnchor)
                    c.mergeCharFormat(fmt)
                it += 1
            block = block.next()

        cursor.endEditBlock()

        # Restore cursor position
        total_len = len(self.editor.toPlainText())
        c_restore = self.editor.textCursor()
        c_restore.setPosition(min(orig_anchor, total_len))
        c_restore.setPosition(min(orig_pos, total_len), QTextCursor.MoveMode.KeepAnchor)
        self.editor.setTextCursor(c_restore)
        self.editor.setFontPointSize(new_size)

    def increase_font_size(self):
        if self.font_size < 32:
            self.font_size += 1
            self._apply_font_size_to_document(self.font_size)
            self._update_font_display()
            self.save_now()

    def decrease_font_size(self):
        if self.font_size > 8:
            self.font_size -= 1
            self._apply_font_size_to_document(self.font_size)
            self._update_font_display()
            self.save_now()

    def _update_font_display(self):
        if hasattr(self, "font_size_label"):
            self.font_size_label.setText(f"{self.font_size}pt")

    def toggle_bold(self):
        w = QFont.Weight.Bold if self.editor.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal
        self.editor.setFontWeight(w)

    def toggle_italic(self):
        self.editor.setFontItalic(not self.editor.fontItalic())

    def toggle_underline(self):
        self.editor.setFontUnderline(not self.editor.fontUnderline())

    def insert_table_dialog(self):
        """Insert a formatted table via dialog."""
        dlg = TableDialog(self)
        if dlg.exec():
            rows, cols = dlg.get_dimensions()
            cursor = self.editor.textCursor()
            table_format = QTextTableFormat()
            table_format.setBorder(1)
            table_format.setCellPadding(6)
            table_format.setCellSpacing(0)
            cursor.insertTable(rows, cols, table_format)

    def _copy_specific_image(self, img_src: str):
        """Copy a specific right-clicked image to clipboard."""
        if "base64," in img_src:
            match = re.search(r'base64,([A-Za-z0-9+/=]+)', img_src)
            if match:
                raw = base64.b64decode(match.group(1))
                img = QImage()
                if img.loadFromData(raw):
                    QApplication.clipboard().setImage(img)
                    self.show_toast("📋 Image copied to clipboard!", duration=1500)
                    return
        self.show_toast("⚠️ Could not copy image", duration=1500)

    def _save_specific_image(self, img_src: str):
        """Save a right-clicked image to disk."""
        if "base64," in img_src:
            match = re.search(r'base64,([A-Za-z0-9+/=]+)', img_src)
            if match:
                raw = base64.b64decode(match.group(1))
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Save Image", "screenshot.png", "PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*.*)"
                )
                if file_path:
                    try:
                        with open(file_path, "wb") as f:
                            f.write(raw)
                        self.show_toast("💾 Image saved successfully!", duration=1800)
                    except Exception as e:
                        self.show_toast(f"⚠️ Error saving image: {e}", duration=2500)

    def insert_image_dialog(self):
        """Open file dialog to insert an image file from disk."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image to Insert", "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.webp);;All Files (*.*)"
        )
        if file_path:
            img = QImage(file_path)
            if not img.isNull():
                self.editor.insert_image(img)
                self.save_now()
                self.show_toast("🖼️ Image inserted!", duration=1500)

    def _delete_selected_image(self):
        """Delete currently selected image."""
        if self.editor.selected_image_pos != -1:
            c = self.editor.textCursor()
            c.setPosition(self.editor.selected_image_pos)
            c.setPosition(self.editor.selected_image_pos + 1, QTextCursor.MoveMode.KeepAnchor)
            c.removeSelectedText()
            self.editor.selected_image_pos = -1
            self.editor.viewport().update()
            self.save_now()
            self.show_toast("🗑️ Image removed", duration=1500)

    def _show_context_menu(self, pos):
        """Context menu with screenshot copy, image insertion, and table tools."""
        menu = self.editor.createStandardContextMenu()
        menu.addSeparator()

        # Check if right-clicked directly on an image
        cursor = self.editor.cursorForPosition(pos)
        fmt = cursor.charFormat()
        img_fmt = fmt.toImageFormat() if fmt.isImageFormat() else None

        if img_fmt and img_fmt.name():
            self.editor.selected_image_pos = cursor.position()
            self.editor.viewport().update()
            img_src = img_fmt.name()

            # Preset resize options
            resize_menu = menu.addMenu("📐 Resize Image")
            fit_act = resize_menu.addAction("Fit Note Width")
            fit_act.triggered.connect(lambda: self.editor.set_selected_image_size(max(180, self.editor.viewport().width() - 24)))
            p100_act = resize_menu.addAction("Reset to Standard (340px)")
            p100_act.triggered.connect(lambda: self.editor.set_selected_image_size(340))
            p75_act = resize_menu.addAction("75% of Current Size")
            p75_act.triggered.connect(lambda: self.editor.set_selected_image_size(int((self.editor.get_selected_image_rect().width() if self.editor.get_selected_image_rect() else 300) * 0.75)))
            p50_act = resize_menu.addAction("50% of Current Size")
            p50_act.triggered.connect(lambda: self.editor.set_selected_image_size(int((self.editor.get_selected_image_rect().width() if self.editor.get_selected_image_rect() else 300) * 0.5)))

            copy_img_action = menu.addAction("📋 Copy This Image")
            copy_img_action.triggered.connect(lambda: self._copy_specific_image(img_src))

            save_img_action = menu.addAction("💾 Save Image As...")
            save_img_action.triggered.connect(lambda: self._save_specific_image(img_src))

            del_img_action = menu.addAction("🗑️ Delete Image")
            del_img_action.triggered.connect(self._delete_selected_image)
            menu.addSeparator()

        # Copy note as screenshot
        snap_action = menu.addAction("📸 Copy Note as Screenshot")
        snap_action.setShortcut(QKeySequence(f"{MOD_KEY}+Shift+C"))
        snap_action.triggered.connect(self.copy_note_as_screenshot)

        # Insert Image
        img_action = menu.addAction("🖼️ Insert Image...")
        img_action.triggered.connect(self.insert_image_dialog)

        # Insert Table
        table_action = menu.addAction("📊 Insert Table...")
        table_action.triggered.connect(self.insert_table_dialog)

        menu.addSeparator()
        clear_action = menu.addAction("🗑️ Clear Note")
        clear_action.triggered.connect(self.clear_all_text)

        menu.exec(self.editor.mapToGlobal(pos))

    def show_toast(self, message: str, show_undo: bool = False, duration: int = 2000):
        """Display notification / undo toast banner."""
        self.toast_label.setText(message)
        if show_undo:
            self.undo_btn.show()
        else:
            self.undo_btn.hide()
        self.toast_banner.show()
        self.toast_timer.start(duration)

    def hide_toast(self):
        self.toast_banner.hide()

    def is_mouse_over_window(self) -> bool:
        """Check if global cursor position is currently hovering on top of the window."""
        try:
            if not self.isVisible() or self.isMinimized():
                return False
            cursor_pos = QCursor.pos()
            # frameGeometry covers window borders and title bar; geometry covers client area
            if self.frameGeometry().contains(cursor_pos) or self.geometry().contains(cursor_pos):
                return True
            # Also verify via widget-local coordinate mapping
            return self.rect().contains(self.mapFromGlobal(cursor_pos))
        except Exception:
            return False

    def eventFilter(self, watched, event):
        """Monitor user interactions to wake window and reset idle countdown."""
        EV_TYPES = (
            QEvent.Type.MouseMove,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.MouseButtonRelease,
            QEvent.Type.KeyPress,
            QEvent.Type.KeyRelease,
            QEvent.Type.Wheel,
            QEvent.Type.FocusIn,
            QEvent.Type.Enter,
            QEvent.Type.HoverEnter,
            QEvent.Type.HoverMove,
        )
        if event.type() in EV_TYPES:
            self.wake_from_idle()
        return super().eventFilter(watched, event)

    def enterEvent(self, event):
        self.wake_from_idle()
        super().enterEvent(event)

    def wake_from_idle(self):
        """Restore window to 100% opacity smoothly and restart idle timer."""
        if self.is_dimmed or self.windowOpacity() < 1.0:
            self.is_dimmed = False
            self.opacity_anim.stop()
            self.opacity_anim.setStartValue(self.windowOpacity())
            self.opacity_anim.setEndValue(1.0)
            self.opacity_anim.start()
        if self.idle_enabled:
            self.inactivity_timer.start(self.idle_timeout_seconds * 1000)

    def _on_inactivity_timeout(self):
        """Dim window when user has been idle for the configured runout duration."""
        if not self.idle_enabled or self.is_dimmed:
            return
        # Don't dim if user has an active modal dialog open
        if QApplication.activeModalWidget() is not None:
            self.inactivity_timer.start(self.idle_timeout_seconds * 1000)
            return
        # Don't dim if mouse cursor is currently on top of the PinNote window
        if self.is_mouse_over_window():
            self.inactivity_timer.start(self.idle_timeout_seconds * 1000)
            return

        self.is_dimmed = True
        target_opacity = max(0.2, min(1.0, self.idle_opacity / 100.0))
        self.opacity_anim.stop()
        self.opacity_anim.setStartValue(self.windowOpacity())
        self.opacity_anim.setEndValue(target_opacity)
        self.opacity_anim.start()

    def open_settings(self):
        """Show clean, compact popup Settings menu right above the gear button."""
        self.wake_from_idle()
        menu = QMenu(self)
        menu.setFont(get_app_font(9))

        # 1. Start on boot toggle
        boot_label = "Start on system boot" if sys.platform == "darwin" else "Start on Windows boot"
        boot_act = QAction(boot_label, menu)
        boot_act.setCheckable(True)
        boot_act.setChecked(self.start_on_boot)
        boot_act.toggled.connect(self._on_menu_boot_toggled)
        menu.addAction(boot_act)

        menu.addSeparator()

        # 2. Idle Transparency toggle
        idle_act = QAction("Auto-transparency when idle", menu)
        idle_act.setCheckable(True)
        idle_act.setChecked(self.idle_enabled)
        idle_act.toggled.connect(self._on_menu_idle_toggled)
        menu.addAction(idle_act)

        # 3. Runout time submenu
        time_menu = menu.addMenu("Runout time")
        time_menu.setEnabled(self.idle_enabled)
        time_group = QActionGroup(self)
        time_group.setExclusive(True)

        timeout_options = [
            ("5 seconds", 5),
            ("15 seconds", 15),
            ("30 seconds", 30),
            ("45 seconds", 45),
            ("1 minute", 60),
            ("2 minutes", 120),
            ("3 minutes", 180),
            ("5 minutes", 300),
            ("10 minutes", 600),
        ]
        for label, secs in timeout_options:
            act = QAction(label, time_menu)
            act.setCheckable(True)
            act.setChecked(self.idle_timeout_seconds == secs)
            act.setData(secs)
            time_group.addAction(act)
            time_menu.addAction(act)
            act.triggered.connect(lambda checked, s=secs: self._set_idle_timeout(s))

        # 4. Idle Opacity submenu
        op_menu = menu.addMenu("Idle opacity")
        op_menu.setEnabled(self.idle_enabled)
        op_group = QActionGroup(self)
        op_group.setExclusive(True)

        opacity_options = [
            ("20% (Very Faint)", 20),
            ("30% Opacity", 30),
            ("40% Opacity", 40),
            ("50% Opacity (Standard)", 50),
            ("60% Opacity", 60),
            ("70% Opacity", 70),
            ("80% Opacity (Subtle)", 80),
        ]
        for label, pct in opacity_options:
            act = QAction(label, op_menu)
            act.setCheckable(True)
            act.setChecked(self.idle_opacity == pct)
            act.setData(pct)
            op_group.addAction(act)
            op_menu.addAction(act)
            act.triggered.connect(lambda checked, p=pct: self._set_idle_opacity(p))

        menu.addSeparator()

        # 5. Version info
        ver_act = QAction("PinNote v1.1", menu)
        ver_act.setEnabled(False)
        menu.addAction(ver_act)

        # Pop up menu aligned directly above the settings button
        btn_pos = self.settings_btn.mapToGlobal(QPoint(0, 0))
        menu_hint = menu.sizeHint()
        popup_x = max(10, btn_pos.x() - menu_hint.width() + self.settings_btn.width())
        popup_y = btn_pos.y() - menu_hint.height() - 4
        menu.exec(QPoint(popup_x, popup_y))

    def _on_menu_boot_toggled(self, checked):
        self.start_on_boot = checked
        set_start_on_boot(checked)
        self.save_now()
        sys_name = "Mac" if sys.platform == "darwin" else "Windows"
        msg = f"✓ PinNote will open on {sys_name} boot" if checked else "Removed from startup"
        self.show_toast(msg, duration=1500)

    def _on_menu_idle_toggled(self, checked):
        self.idle_enabled = checked
        self.save_now()
        if checked:
            self.inactivity_timer.start(self.idle_timeout_seconds * 1000)
            self.show_toast("✓ Auto-transparency enabled", duration=1500)
        else:
            self.inactivity_timer.stop()
            self.setWindowOpacity(1.0)
            self.is_dimmed = False
            self.show_toast("Auto-transparency disabled", duration=1500)

    def _set_idle_timeout(self, secs):
        self.idle_timeout_seconds = secs
        self.save_now()
        if self.idle_enabled:
            self.inactivity_timer.start(self.idle_timeout_seconds * 1000)
        label = f"{secs}s" if secs < 60 else f"{secs // 60}m"
        self.show_toast(f"✓ Runout time set to {label}", duration=1500)

    def _set_idle_opacity(self, pct):
        self.idle_opacity = pct
        self.save_now()
        self.show_toast(f"✓ Idle opacity set to {pct}%", duration=1500)
        # Briefly preview the opacity for 800ms so user sees the transparency level
        self.setWindowOpacity(pct / 100.0)
        QTimer.singleShot(800, lambda: self.setWindowOpacity(1.0))

    def save_now(self, show_feedback: bool = False):
        """Commit note content and settings to disk."""
        html_content = self.editor.toHtml()
        plain_content = self.editor.toPlainText()
        geo = self.geometry()
        geom_str = f"{geo.width()}x{geo.height()}+{geo.x()}+{geo.y()}"

        payload = {
            "html": html_content,
            "text": plain_content,
            "theme": self.theme,
            "always_on_top": self.is_pinned,
            "geometry": geom_str,
            "font_size": self.font_size,
            "start_on_boot": self.start_on_boot,
            "idle_transparency_enabled": self.idle_enabled,
            "idle_timeout_seconds": self.idle_timeout_seconds,
            "idle_opacity": self.idle_opacity,
        }

        success = save_data(payload)
        t = THEMES[self.theme]
        if success:
            self.status_label.setText("● Saved")
            self.status_label.setStyleSheet(f"color: {t['success']};")
            if show_feedback:
                self.show_toast("✓ Saved to disk", duration=1200)
        else:
            self.status_label.setText("⚠️ Error")
            self.status_label.setStyleSheet(f"color: {t['danger']};")

    def closeEvent(self, event):
        self.save_now()
        event.accept()


def main():
    if sys.platform == "win32":
        try:
            import ctypes
            myappid = "pinnote.minimalist.stickynote.v1"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)
    if sys.platform == "darwin":
        app.setApplicationName("PinNote")
        app.setDesktopFileName("PinNote")
        icon_path = get_asset_path("icon.icns")
        if not os.path.exists(icon_path):
            icon_path = get_asset_path("icon.png")
    else:
        icon_path = get_asset_path("icon.ico")
        if not os.path.exists(icon_path):
            icon_path = get_asset_path("icon.png")

    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = PinNoteApp()
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    window.show()
    window.raise_()
    window.activateWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
