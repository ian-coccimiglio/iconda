import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import subprocess

class CondaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conda Environment Manager")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        
        list_button = QPushButton("List Environments")
        list_button.clicked.connect(self.list_environments)
        layout.addWidget(list_button)

        create_button = QPushButton("Create Environment")
        create_button.clicked.connect(self.create_environment)
        layout.addWidget(create_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def list_environments(self):
        result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
        print(result.stdout)

    def create_environment(self):
        # Add logic to get environment name from user
        env_name = "my_new_env"
        result = subprocess.run(['conda', 'create', '-n', env_name, '-y'], capture_output=True, text=True)
        print(result.stdout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CondaGUI()
    window.show()
    sys.exit(app.exec_())
