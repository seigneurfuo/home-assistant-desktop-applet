import json
import os.path
import sys
import webbrowser
from pathlib import Path
from pprint import pprint

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QDialog

import requests

class StatusIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.connection_error_count = 0

        self.actions = []

        self.load_config()

        self.setIcon(QIcon.fromTheme("home"))


        # QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.setInterval(self.config["update_interval"])
        self.timer.start()

        self.init_ui()

        self.tick()

    def load_config(self):
        with open(os.path.join(Path.home(), ".config", "home-assistant-indicator.json")) as config_file:
            self.config = json.load(config_file)

    def init_ui(self):
        self.menu = QMenu()

        # Création des élements en fonction du nombre de capteurs
        for sensor in self.config["sensors"]:
            item = self.menu.addAction(QIcon.fromTheme(""), "<EMPTY>")
            self.actions.append(item)

        self.menu.addSeparator()

        open_webbrowser = self.menu.addAction(QIcon.fromTheme("web"), "Ouvrir dans le navigateur")
        open_webbrowser.triggered.connect(self.open_webbrowser)

        close_action = self.menu.addAction(QIcon.fromTheme("close"), "Quitter")
        close_action.triggered.connect(self.close)

        self.setContextMenu(self.menu)

    def tick(self):
        for action_index, sensor in enumerate(self.config["sensors"]):
            sensor_data = self.get_sensor_data(sensor)

            if self.connection_error_count == 3:
                self.connection_error_count = 0

                title = ""
                msg = ""
                self.showMessage(title, msg)

            # Erreur
            if not sensor_data:
                return

            name = sensor_data["attributes"]["friendly_name"]
            state = sensor_data["state"]
            unit = sensor_data["attributes"]["unit_of_measurement"]

            msg = f"{name}: {state}"

            if self.config["show_units"]:
                msg += unit

            # Permet d'afficher l'information du premier capteur dans le tooltip
            if action_index == 0:
                self.setToolTip(msg)

            self.actions[action_index].setText(msg)

    def get_sensor_data(self, entity_id):
        try:
            url = f"{self.config['url']}/api/states/{entity_id}"
            headers = {
                "Authorization": f"Bearer {self.config['key']}",
                "content-type": "application/json",
            }

            response = requests.get(url, headers=headers)
            return response.json()

        except:
            return None

    def open_webbrowser(self):
        webbrowser.open_new_tab(self.config["url"])

    def close(self):
        self.setVisible(False)
        exit(0)

class SettingsWindow(QDialog):
    def __init__(self, parent):
        super(self).__init__()

        self.parent = parent

        self.init_ui()
        self.init_events()

    def init_events(self):
        pass

    def init_ui(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    status_icon = StatusIcon()
    status_icon.setVisible(True)
    app.exec()