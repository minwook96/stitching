from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout


class QImageViewSync(QWidget):
    def __init__(self, window=None):
        super().__init__()

        self.window = window
        self.scaleFactor = 0.0

        self.imageLabelLeft = QLabel()
        self.imageLabelLeft.setBackgroundRole(QPalette.Base)
        self.imageLabelLeft.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabelLeft.setScaledContents(True)

        self.scrollAreaLeft = QScrollArea()
        self.scrollAreaLeft.setBackgroundRole(QPalette.Dark)
        self.scrollAreaLeft.setWidget(self.imageLabelLeft)
        self.scrollAreaLeft.setVisible(False)

        self.centralWidget = QWidget()
        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.addWidget(self.scrollAreaLeft)

        self.scrollAreaLeft.mouseMoveEvent = self.mouseMoveEventLeft
        self.scrollAreaLeft.mousePressEvent = self.mousePressEventLeft
        self.scrollAreaLeft.mouseReleaseEvent = self.mouseReleaseEventLeft

        self.imageLabelLeft.setCursor(Qt.OpenHandCursor)

    def mousePressEventLeft(self, event):
        self.pressed = True
        self.imageLabelLeft.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollAreaLeft.horizontalScrollBar().value() + event.pos().x()
        self.initialPosY = self.scrollAreaLeft.verticalScrollBar().value() + event.pos().y()

    def mouseReleaseEventLeft(self, event):
        self.pressed = False
        self.imageLabelLeft.setCursor(Qt.OpenHandCursor)
        self.initialPosX = self.scrollAreaLeft.horizontalScrollBar().value()
        self.initialPosY = self.scrollAreaLeft.verticalScrollBar().value()

    def mouseMoveEventLeft(self, event):
        if self.pressed:
            self.scrollAreaLeft.horizontalScrollBar().setValue(self.initialPosX - event.pos().x())
            self.scrollAreaLeft.verticalScrollBar().setValue(self.initialPosY - event.pos().y())

    def openLeft(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabelLeft.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollAreaLeft.setVisible(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelLeft.adjustSize()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabelLeft.adjustSize()
        self.scaleFactor = 1.0

    def updateActions(self):
        self.window.zoomInAct.setEnabled(not self.window.fitToWindowAct.isChecked())
        self.window.zoomOutAct.setEnabled(not self.window.fitToWindowAct.isChecked())
        self.window.normalSizeAct.setEnabled(not self.window.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabelLeft.resize(self.scaleFactor * self.imageLabelLeft.pixmap().size())

        self.adjustScrollBar(self.scrollAreaLeft.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollAreaLeft.verticalScrollBar(), factor)

        self.window.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.window.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageViewSync = QImageViewSync(window=self)
        self.setCentralWidget(self.imageViewSync.centralWidget)

        self.createActions(self.imageViewSync)
        self.createMenus()

        self.setWindowTitle("Image View Sync in the Main Window")
        self.resize(1200, 600)

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.imageViewSync.scrollAreaLeft.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.imageViewSync.normalSize()

        self.imageViewSync.updateActions()

    def createActions(self, view):
        self.openLeftAct = QAction("&Open Left...", self, shortcut="Ctrl+O", triggered=view.openLeft)
    
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=view.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=view.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=view.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self,
                                      enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openLeftAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addSeparator()

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
