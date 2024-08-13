import sys, os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
)
import subprocess
from commands import (
    conda_create,
    conda_env_list,
    conda_remove,
    run_in_conda_env,
)

# not actually useful?
# from conda.cli import main_env_create, main_env_config, install
# from conda.testing import conda_cli

home_dir = os.path.expanduser("~")
conda_shell = os.path.join(home_dir, "miniconda3/etc/profile.d/conda.sh")


class CondaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conda Environment Manager")
        self.setGeometry(2200, 600, 300, 200)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        QListWidgetItem("Cellpose", self.list_widget)
        QListWidgetItem("Napari", self.list_widget)
        QListWidgetItem("Jupyter", self.list_widget)
        QListWidgetItem("Spyder", self.list_widget)
        layout.addWidget(self.list_widget)
        self.list_widget.itemSelectionChanged.connect(self.on_change)

        create_button = QPushButton("Create Environment")
        create_button.clicked.connect(self.create_environment)
        layout.addWidget(create_button)

        list_button = QPushButton("List Environments")
        list_button.clicked.connect(self.list_environments)
        layout.addWidget(list_button)

        remove_button = QPushButton("Remove Environment")
        remove_button.clicked.connect(self.remove_environment)
        layout.addWidget(remove_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_change(self):
        print(f"Selected {self.list_widget.selectedItems()[0].text()}")
        # print([item.text() for item in self.list_widget.selectedItems()])

    def create_environment(self):
        # Add logic to get environment name from user
        selected_item_name = self.list_widget.selectedItems()[0].text()
        env_name = selected_item_name + "_test"
        print(f"Creating {env_name} environment")
        print("Working on it...")
        result = conda_create(conda_shell, env_name)
        if result.returncode != 0:
            print("something weird happened")
        print("Installing GUI")
        if "Cellpose" in env_name:
            result = run_in_conda_env(
                conda_shell, env_name, "pip install cellpose[gui]"
            )
        print(f"{env_name} environment created!")

    def list_environments(self):
        conda_env_list(conda_shell)

    def remove_environment(self):
        selected_item_name = self.list_widget.selectedItems()[0].text()
        env_name = selected_item_name + "_test"
        print(f"Removing {env_name} environment")
        result = conda_remove(conda_shell, env_name)
        print(f"{env_name} removed")
        if result.returncode != 0:
            print("something weird happened")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CondaGUI()
    window.show()
    sys.exit(app.exec_())
