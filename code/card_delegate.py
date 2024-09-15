from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtCore import Qt, QSize, QRect, QModelIndex, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QStyledItemDelegate, QListView, QStyleOptionViewItem, QStyle

from card_painter import CardPainter


class CardDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.x_spacing = 10
        self.y_spacing = 10

        self.__is_dragging = False
        self.__is_dragged_index = False
        self.__dragged_index = QModelIndex()

        self.__list_view: QListView = QListView()

        self.__anim_item_rect: QRect = QRect()
        self.__anim_index: QModelIndex = QModelIndex()

        self.__anim_move_down = None
        self.__has_anim_move_down_finished = True

        self.__anim_reduce_width = None
        self.__has_anim_reduce_width_finished = True

    def setDragIndex(self, dragged_index: QModelIndex):
        self.__dragged_index = dragged_index

    def setDragStatus(self, is_dragging: bool):
        self.__is_dragging = is_dragging

    def animStart(self, list_view: QListView, index: QModelIndex, index_rect: QRect):
        self.__anim_move_down = QPropertyAnimation()
        self.__anim_move_down.setDuration(200)
        self.__anim_move_down.setStartValue(index_rect.y())
        self.__anim_move_down.setEasingCurve(QEasingCurve.OutQuad)
        self.__anim_move_down.finished.connect(self.__onMoveDownFinished)
        self.__anim_move_down.valueChanged.connect(self.__onMoveDownValueChange)
        self.__anim_move_down.setEndValue(index_rect.height())

        self.__anim_reduce_width = QPropertyAnimation()
        self.__anim_reduce_width.setDuration(200)
        self.__anim_reduce_width.setStartValue(0)
        self.__anim_reduce_width.setEasingCurve(QEasingCurve.OutQuad)
        self.__anim_reduce_width.finished.connect(self.__onReduceWidthFinished)
        self.__anim_reduce_width.valueChanged.connect(self.__onReduceWidthValueChanged)
        self.__anim_reduce_width.setEndValue(index_rect.width())

        self.__anim_index = index
        self.__list_view = list_view
        self.__anim_item_rect = index_rect

        self.__has_anim_move_down_finished = False
        self.__has_anim_reduce_width_finished = False

        self.__anim_move_down.start()

    def __onMoveDownValueChange(self, v):
        anim_option = QStyleOptionViewItem()
        anim_option.rect = QRect(self.__anim_item_rect.x(), v, self.__anim_item_rect.width(),
                                 self.__anim_item_rect.height())

        self.anim_down_option = anim_option

        if self.__list_view.model():
            count_row = self.__list_view.model().rowCount()
            self.__updateAllIndexByRange(0, count_row)

    def __onMoveDownFinished(self):
        self.__has_anim_move_down_finished = True
        self.__anim_reduce_width.start()

    def __onReduceWidthValueChanged(self, v):
        self.anim_move_var = v
        index_row = self.__anim_index.row()
        if self.__list_view.model():
            count_row = self.__list_view.model().rowCount()
            self.__updateAllIndexByRange(index_row, count_row)

    def __onReduceWidthFinished(self):
        self.__has_anim_reduce_width_finished = True
        self.__list_view.model().removeRow(self.__anim_index.row())

    def __updateAllIndexByRange(self, start, end):
        model = self.__list_view.model()
        for row in range(start, end):
            index = model.index(row, 0)
            self.__list_view.update(index)

    def paint(self, painter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)

        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.__has_anim_move_down_finished and self.__anim_index == index:
            option = self.anim_down_option

        if not self.__has_anim_reduce_width_finished:
            rect: QRect = option.rect
            option.rect = QRect(rect.x() - self.anim_move_var, rect.y(), rect.width(), rect.height())

        if self.__anim_index == index and not self.__has_anim_reduce_width_finished and self.__has_anim_move_down_finished:
            return

        rect: QRect = option.rect
        rect = self.__adjustRect(rect)
        CardPainter.drawBackground(painter,rect,QColor(20, 109, 109) if option.state & QStyle.State_Selected else QColor(45, 134, 134))
        CardPainter.drawText(painter,rect,index)

        if self.__dragged_index == index and self.__is_dragging:
            CardPainter.drawShadow(painter,rect)
            self.__is_dragged_index = True

    def __adjustRect(self, rect: QRect):
        rect = QRect(rect.x() + self.x_spacing,
                     rect.y() + self.y_spacing,
                     rect.width() - self.x_spacing,
                     rect.height() - self.y_spacing)

        return rect

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass

    def destroyEditor(self, editor, index):
        pass

    def sizeHint(self, option: QStyleOptionViewItem, index):
        return QSize(210, 260)
