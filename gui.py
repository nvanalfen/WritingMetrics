import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt
import subprocess

test_file_loc = "/media/nvanalfen/T7/Coding/WritingMetrics/files/test.txt"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tab1 = WritingProjectTabWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Projects")
        self.tabs.addTab(self.tab2, "Metrics")

        # self.layout1 = QVBoxLayout()
        # self.label1 = QLabel("This is Tab 1")
        # self.layout1.addWidget(self.label1)
        # self.tab1.setLayout(self.layout1)

        self.layout2 = QVBoxLayout()
        self.label2 = QLabel("This is Tab 2")
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout2.addWidget(self.label2)
        self.layout2.addWidget(self.text_edit)
        self.tab2.setLayout(self.layout2)

        self.add_text_to_tab2("Click me to run a command!", self.run_command)

        self.setCentralWidget(self.tabs)

    def add_text_to_tab2(self, text, callback):
        clickable_text = QLabel(text)
        clickable_text.setCursor(Qt.PointingHandCursor)
        clickable_text.mousePressEvent = lambda event: callback()
        self.text_edit.append("")
        self.layout2.addWidget(clickable_text)

    def run_command(self):
        self.text_edit.append("Running a command!")

class WritingProjectTabWidget(QWidget):
    def __init__(self, project_dict=None):
        super().__init__()
        self.project_dict = project_dict
        if self.project_dict is None:
            self.project_dict = {}
        self.layout = QVBoxLayout()
        # self.label = QLabel("This is Tab 1")
        # self.layout.addWidget(self.label)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.setLayout(self.layout)
        self.layout.addWidget(self.scroll_area)

        self.set_up_screen()

    def set_up_screen(self):
        links = self.project_dict

        inds = 0
        for key in links:
            clickable_text = QLabel(key)
            clickable_text.setCursor(Qt.PointingHandCursor)
            if links[key] is None:
                clickable_text.mousePressEvent = lambda event: self.print_message()
            else:
                clickable_text.mousePressEvent = lambda event, t=key: self.open_project( links[key] )
            self.scroll_layout.addWidget(clickable_text)

    def add_clickable_text(self, text):
        pass

    def print_message(self, msg=None):
        if msg is None:
            msg = "No path to file"
        print(msg)

    def open_project(self, project_link):
        try:
            subprocess.run(["xdg-open", project_link], shell=False)
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
