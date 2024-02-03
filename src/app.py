import json
import os.path
import sys
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

import requests

class StatusIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.actions = []

        self.load_config()

        self.setIcon(QIcon.fromTheme("home"))

        # QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start()
        self.timer.setInterval(self.config["update_interval"])

        self.init_ui()

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

        close_action = self.menu.addAction(QIcon.fromTheme("close"), "Quitter")
        close_action.triggered.connect(self.close)

        self.setContextMenu(self.menu)

    def tick(self):
        for action_index, sensor in enumerate(self.config["sensors"]):
            name, state = self.get_sensor_state(sensor)
            msg = f"{name}: {state}"

            # Permet d'afficher l'information du premier capteur
            if action_index == 0:
                self.setToolTip(str(state))

            self.actions[action_index].setText(msg)

    def get_sensor_state(self, entity_id):
        url = f"{self.config['api_entrypoint']}/states/{entity_id}"
        headers = {
            "Authorization": f"Bearer {self.config['key']}",
            "content-type": "application/json",
        }

        response = requests.get(url, headers=headers)
        json_response = response.json()
        name = json_response["attributes"]["friendly_name"]
        state = json_response["state"]

        return name, state

    def close(self):
        self.setVisible(False)
        exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    status_icon = StatusIcon()
    status_icon.setVisible(True)
    app.exec()