import os
from PySide6.QtGui import QFont, QFontDatabase, QImage, QPainter, QColor,QPainterPath
from PySide6.QtCore import Qt, QRectF
import tempfile
#os.environ["QT_QPA_PLATFORM"] = "offscreen"

def create_image_qt_text_bg(
    text,
    font_path=None,
    font_family="Arial",
    font_size=40,
    text_color=(255, 255, 255),
    bg_color=None,          # RGB tuple
    bg_opacity=0.5,         # 0.0 to 1.0
    padding=20,
    corner_radius=7.5
):
    # Register custom font
    if font_path:
        font_id = QFontDatabase.addApplicationFont(font_path)
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            font_family = families[0]

    font = QFont(font_family, font_size)

    # Temporary image to measure text size
    temp_img = QImage(1, 1, QImage.Format_ARGB32)
    painter = QPainter(temp_img)
    painter.setFont(font)
    text_rect = painter.boundingRect(0, 0, 1000, 1000, Qt.AlignLeft | Qt.TextWordWrap, text)
    painter.end()

    # Final image size includes padding
    img_width = text_rect.width() + padding * 2
    img_height = text_rect.height() + padding * 2

    img = QImage(img_width, img_height, QImage.Format_ARGB32)
    img.fill(Qt.transparent)

    painter = QPainter(img)
    painter.setFont(font)

    # Draw rounded background rectangle with alpha
    if bg_color:
        r, g, b = bg_color
        alpha = int(bg_opacity * 255)  # Convert to 0–255
        bg_rect = QRectF(padding, padding, text_rect.width(), text_rect.height())
        path = QPainterPath()
        path.addRoundedRect(bg_rect, corner_radius, corner_radius)
        painter.fillPath(path, QColor(r, g, b, alpha))

    # Draw centered text
    painter.setPen(QColor(*text_color))
    painter.drawText(QRectF(padding, padding, text_rect.width(), text_rect.height()),
                     text, Qt.AlignCenter | Qt.TextWordWrap)

    painter.end()

    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_file.name)
    temp_file.close()
    return temp_file.name
