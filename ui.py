import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QComboBox
import qimage2ndarray
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from graph import BFS, DFS, Grid
from PySide6.QtCore import QObject, Signal, Slot

COLORS = {
    'VISITED' : 255,
    'UNVISITED': 0,
    'OBSTACLE': 130
}

class Communicate(QObject):
    term = Signal(str)

@Slot(str)
def reset(info):
    print(info)
    global win
    print(type(win))
    win.matrix = np.zeros((5,5))
    win.fs = False
    win.algo.setEnabled(True)

class AlgoVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.matrix = np.zeros((5,5))

        self.algo = QComboBox()
        self.algo.addItems(['BFS', 'DFS'])

        self.image_label = QLabel()
        self.image_label.setFixedSize(500, 500)

        self.but = QPushButton('Next Step')
        self.but.clicked.connect(self.next_step)

        self.__update_image()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.algo)
        self.main_layout.addWidget(self.but)
        self.setLayout(self.main_layout)

        self.fs = False
        self.com = Communicate()
        self.com.term.connect(reset)

    def __update_image(self):
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.imshow(self.matrix)
            ax.set_title('Traversal')
            canvas.draw()

            width, height = fig.figbbox.width, fig.figbbox.height
            img = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
            pixmap = QPixmap(img)

            self.image_label.setPixmap(pixmap)

    def next_step(self):
        if self.fs == False:
            self.algo.setEnabled(False)
            self.fs = True
            if self.algo.currentText() == 'BFS':
                self.trav = BFS(Grid(5,5, set([(1,1), (2,2), (3,3)])))
            elif self.algo.currentText() == 'DFS':
                self.trav = DFS(Grid(5,5, set()))
            else:
                pass

            for x in self.trav.grid.obstacles:
                self.matrix[x[0]][x[1]] = COLORS['OBSTACLE']

        curr = next(self.trav.traverse())
        if curr != None:
            self.matrix[curr[0]][curr[1]] = COLORS['VISITED']
        else:
            self.com.term.emit('Ok')

        self.__update_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    global win
    win = AlgoVisualizer()
    win.show()
    sys.exit(app.exec())
