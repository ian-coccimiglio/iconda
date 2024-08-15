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
from commands import (
    conda_create,
    conda_env_list,
    conda_remove,
    run_in_conda_env,
    conda_env_exists,
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
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        curated_envs = ["cellpose_test", "Napari_test", "Jupyter_test"]
        for env in curated_envs:
            if conda_env_exists(conda_shell, env):
                env += "\t[Installed]"
            else:
                env += "\t[Uninstalled]"
            QListWidgetItem(env, self.list_widget)
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

    def dragEnterEvent(self, event):
         if event.mimeData().hasUrls():
             event.accept()
         else:
             event.ignore()
    
    def dropEvent(self, event):
         files = [u.toLocalFile() for u in event.mimeData().urls()]
         for file in files:
             QListWidgetItem(file, )
             self.list_widget.addItem
         

    def on_change(self):
        selected_item = self.list_widget.selectedItems()[0]

    #        print(f"Selected {selected_item.text()}")
    #        selected_item.setText(selected_item.text() + "\t[selected]")

    # print([item.text() for item in self.list_widget.selectedItems()])

    def create_environment(self):
        # Add logic to get environment name from user
        if not self.list_widget.selectedItems():
            print("Select an item first")
            return None
        selected_item_name = self.list_widget.selectedItems()[0]
        if "[Installed]" in selected_item_name.text():
            print("Environment is already installed!")
            return None
        else:
            env_name = selected_item_name.text().split("\t")[0]
        print(f"Creating {env_name} environment")
        print("Working on it...")
        from_environment = False

        if "Cellpose" in env_name:
            from_environment = True

        result = conda_create(conda_shell, env_name, from_environment)

        if "Cellpose" in env_name:
            print("Installing GUI")
            result = run_in_conda_env(
                conda_shell, env_name, "pip install cellpose[gui]"
            )
        print(f"{env_name} environment created!")
        if conda_env_exists(conda_shell, env_name):
            selected_item_name.setText(env_name + "\t[Installed]")

    def list_environments(self):
        conda_env_list(conda_shell)

    def remove_environment(self):
        selected_item_name = self.list_widget.selectedItems()[0]
        env_name = selected_item_name.text().split("\t")[0]
        print(f"Removing {env_name} environment")
        result = conda_remove(conda_shell, env_name)
        print(f"{env_name} removed")
        if conda_env_exists(conda_shell, env_name):
            print("Environment wasn't removed")
        else:
            selected_item_name.setText(env_name + "\t[Uninstalled]")

        if result.returncode != 0:
            print("something weird happened")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CondaGUI()
    window.show()
    sys.exit(app.exec_())
