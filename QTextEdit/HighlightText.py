import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCharFormat, QTextDocument, QTextCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QToolBar, QLineEdit, QPushButton, QColorDialog, QHBoxLayout, QWidget)


class TextEdit(QMainWindow):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        widget = QWidget(self)
        vb = QHBoxLayout(widget)
        vb.setContentsMargins(0, 0, 0, 0)
        self.findText = QLineEdit(self)
        self.findText.setText('self')
        findBtn = QPushButton('高亮', self)
        findBtn.clicked.connect(self.highlight)
        vb.addWidget(self.findText)
        vb.addWidget(findBtn)

        tb = QToolBar(self)
        tb.addWidget(widget)
        self.addToolBar(tb)

    def setText(self, text):
        self.textEdit.setPlainText(text)

    def highlight(self):
        text = self.findText.text()  # 文 输入 中 中 
        if not text:
            return

        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        # 기본 색상을 복원합니다 
        cursor = self.textEdit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        self.textEdit.setTextCursor(cursor)

        # 文 
        fmt = QTextCharFormat()
        fmt.setForeground(col)

        # 正 则 
        expression = QRegExp(text)
        self.textEdit.moveCursor(QTextCursor.Start)
        cursor = self.textEdit.textCursor()

        # 循 查 设置 设置 设置. 
        pos = 0
        index = expression.indexIn(self.textEdit.toPlainText(), pos)
        while index >= 0:
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.Right,
                                QTextCursor.KeepAnchor, len(text))
            cursor.mergeCharFormat(fmt)
            pos = index + expression.matchedLength()
            index = expression.indexIn(self.textEdit.toPlainText(), pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    textEdit = TextEdit()
    textEdit.resize(800, 600)
    textEdit.show()
    textEdit.setText(open(sys.argv[0], 'rb').read().decode())

    sys.exit(app.exec_())
