import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matplotlib in PyQt5')

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create a button to update the plot
        self.update_button = QPushButton('Update Plot', self)
        self.update_button.clicked.connect(self.update_plot)
        layout.addWidget(self.update_button)

        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.nav_toolbar)

        self.plot_data()

    def plot_data(self):
        # Example plot data
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 2, 7, 4]
        self.ax.plot(x, y)
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Matplotlib Plot')

        self.canvas.draw()

    def update_plot(self):
        # Example: Update the plot when the button is clicked
        x = [1, 2, 3, 4, 5]
        new_y = [5, 4, 3, 6, 2]
        self.ax.clear()
        self.ax.plot(x, new_y)
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Updated Matplotlib Plot')

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
