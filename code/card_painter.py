from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtCore import Qt, QRect, QModelIndex, QObject


class CardPainter(QObject):
    @classmethod
    def drawBackground(cls, painter: QPainter, rect: QRect, color: QColor):
        painter.save()
        painter.setBrush(color)
        painter.drawRoundedRect(rect, 10, 10)
        painter.restore()

    @classmethod
    def drawShadow(cls, painter: QPainter, rect: QRect):
        painter.save()
        painter.setBrush(QColor(0, 0, 0, 100))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        painter.restore()

    @classmethod
    def drawText(cls, painter: QPainter, rect: QRect, index: QModelIndex):
        card_data = index.data(Qt.DisplayRole)
        if not isinstance(card_data, dict):
            return

        title = card_data.get("title", "")
        description = card_data.get("description", "")

        painter.save()

        title_rect = rect.adjusted(10, 10, -10, -30)
        description_rect = rect.adjusted(10, 50, -10, -10)

        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(font)
        painter.drawText(title_rect, Qt.AlignLeft | Qt.TextWordWrap, title)

        font = QFont("Corbel", 11)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(description_rect, Qt.AlignLeft | Qt.TextWordWrap, description)

        painter.restore()
