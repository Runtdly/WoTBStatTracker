import json
import requests
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGridLayout, QFormLayout, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QScreen

APP_ID = "fab97ea7728dfb15463f1af276cef479"
API = "https://api.wotblitz.eu/wotb/account/"
player = "BABAJAGHJAAA"

def get_player_id() -> str:
	data = requests.get(f"{API}/list/?application_id={APP_ID}&search={player}")
	json_data = json.loads(data.text)
	data = json_data['data']
	acc_id = data[0]['account_id']

	return acc_id


def get_stats() -> dict:
	acc_id = get_player_id()

	data = requests.get(f"{API}/info/?application_id={APP_ID}&account_id={acc_id}")
	json_data = json.loads(data.text)
	data = json_data['data']
	player_id_data = data[f"{acc_id}"]
	statistics = player_id_data['statistics']
	all_stats = statistics['all']

	#General battle
	wins = all_stats['wins']
	battles = all_stats['battles']

	#General personal
	kills = all_stats['frags']
	survived = all_stats['survived_battles']
	survived_wins = all_stats['win_and_survived']
	spots = all_stats['spotted']
	dmg_dealt = all_stats['damage_dealt']
	dmg_received = all_stats['damage_received']
	cap = all_stats['capture_points']
	decap = all_stats['dropped_capture_points']
	hits = all_stats['hits']
	shots = all_stats['shots']
	xp = all_stats['xp']

	#Calculated values
	deaths = battles - survived
	winrate = wins / battles * 100
	dmg_ratio = dmg_dealt / dmg_received
	kd_ratio = kills / deaths

	dmg_battle = dmg_dealt / battles
	hurt_battle = dmg_received / battles
	kills_battle = kills / battles
	spots_battle = spots / battles
	hits_battle = hits / battles
	shots_battle = shots / battles
	cap_battle = cap / battles
	decap_battle = decap /battles

	player_stats = {
		"battles": battles,
		"wins": wins,
		"kills": kills,
		"survived": survived,
		"survived_wins": survived_wins,
		"spots": spots,
		"dmg_dealt": dmg_dealt,
		"dmg_received": dmg_received,
		"cap": cap,
		"decap": decap,
		"hits": hits,
		"shots": shots,
		"xp": xp,
		"deaths": deaths,
		"winrate": winrate,
		"dmg_ratio": dmg_ratio,
		"kd_ratio": kd_ratio,
		"dmg_battle": dmg_battle,
		"hurt_battle": hurt_battle,
		"kills_battle": kills_battle,
		"spots_battle": spots_battle,
		"hits_battle": hits_battle,
		"shots_battle": shots_battle,
		"cap_battle": cap_battle,
		"decap_battle": decap_battle
	}

	return player_stats


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("Session Tracker")
		self.setStyleSheet("background-color: black; color: rgb(255,255,255)")
		self.setGeometry(500,500,700,100)
		self.start_session = get_stats()

		font = self.font()
		font.setPointSize(20)
		font.setBold(True)

		#Layout
		centralWidget = QWidget(self)
		self.setCentralWidget(centralWidget)
		layout = QGridLayout(centralWidget)
		centralWidget.setLayout(layout)

		#Label Widgets
		self.battlesWidget = QLabel(centralWidget)
		self.battlesWidget.setText("B:")
		self.battlesWidget.setFont(font)
		self.battlesWidget.setAlignment(Qt.AlignCenter)

		self.winrateWidget = QLabel(centralWidget)
		self.winrateWidget.setText("WR:")
		self.winrateWidget.setFont(font)
		self.winrateWidget.setAlignment(Qt.AlignCenter)

		self.dmgWidget = QLabel(centralWidget)
		self.dmgWidget.setText("DMG:")
		self.dmgWidget.setFont(font)
		self.dmgWidget.setAlignment(Qt.AlignCenter)

		self.drWidget = QLabel(centralWidget)
		self.drWidget.setText("DR:")
		self.drWidget.setFont(font)
		self.drWidget.setAlignment(Qt.AlignCenter)

		self.kdWidget = QLabel(centralWidget)
		self.kdWidget.setText("K/D:")
		self.kdWidget.setFont(font)
		self.kdWidget.setAlignment(Qt.AlignCenter)

		#Value Widgets
		self.battlesValue = QLabel(centralWidget)
		self.battlesValue.setText("-")
		self.battlesValue.setFont(font)
		self.battlesValue.setAlignment(Qt.AlignCenter)

		self.winrateValue = QLabel(centralWidget)
		self.winrateValue.setText("-")
		self.winrateValue.setFont(font)
		self.winrateValue.setAlignment(Qt.AlignCenter)

		self.dmgValue = QLabel(centralWidget)
		self.dmgValue.setText("-")
		self.dmgValue.setFont(font)
		self.dmgValue.setAlignment(Qt.AlignCenter)

		self.drValue = QLabel(centralWidget)
		self.drValue.setText("-")
		self.drValue.setFont(font)
		self.drValue.setAlignment(Qt.AlignCenter)

		self.kdValue = QLabel(centralWidget)
		self.kdValue.setText("-")
		self.kdValue.setFont(font)
		self.kdValue.setAlignment(Qt.AlignCenter)



		#Adding the widgets to the layout
		layout.addWidget(self.battlesWidget, 0, 0)
		layout.addWidget(self.winrateWidget, 0, 1)
		layout.addWidget(self.dmgWidget, 0, 2)
		layout.addWidget(self.drWidget, 0, 3)
		layout.addWidget(self.kdWidget, 0, 4)

		layout.addWidget(self.battlesValue, 1, 0)
		layout.addWidget(self.winrateValue, 1, 1)
		layout.addWidget(self.dmgValue, 1, 2)
		layout.addWidget(self.drValue, 1, 3)
		layout.addWidget(self.kdValue, 1, 4)


		#Updating the results
		self.update_timer = QTimer()
		self.update_timer.start(5000)
		self.update_timer.setSingleShot(False)
		self.update_timer.timeout.connect(self.update_session)


	def update_session(self) -> None:
		current_session = get_stats()

		battles = current_session.get('battles') - self.start_session.get('battles')
		wins = current_session.get('wins') - self.start_session.get('wins')
		kills = current_session.get('kills') - self.start_session.get('kills')
		deaths = current_session.get('deaths') - self.start_session.get('deaths')
		spots = current_session.get('spots') - self.start_session.get('spots')
		dmg_dealt = current_session.get('dmg_dealt') - self.start_session.get('dmg_dealt')
		dmg_received = current_session.get('dmg_received') - self.start_session.get('dmg_received')
		cap = current_session.get('cap') - self.start_session.get('cap')
		decap = current_session.get('decap') - self.start_session.get('decap')
		hits = current_session.get('hits') - self.start_session.get('hits')
		shots = current_session.get('shots') - self.start_session.get('shots')
		xp = current_session.get('xp') - self.start_session.get('xp')
		
		winrate_gain = current_session.get('winrate') - self.start_session.get('winrate')
		dmg_ratio_gain = current_session.get('dmg_ratio') - self.start_session.get('dmg_ratio')
		kd_ratio_gain = current_session.get('kd_ratio') - self.start_session.get('kd_ratio')

		dmg_battle_gain = current_session.get('dmg_battle') - self.start_session.get('dmg_battle')
		hurt_battle_gain = current_session.get('hurt_battle') - self.start_session.get('hurt_battle')
		kills_battle_gain = current_session.get('kills_battle') - self.start_session.get('kills_battle')
		spots_battle_gain = current_session.get('spots_battle') - self.start_session.get('spots_battle')
		hits_battle_gain = current_session.get('hits_battle') - self.start_session.get('hits_battle')
		shots_battle_gain = current_session.get('shots_battle') - self.start_session.get('shots_battle')
		cap_battle_gain = current_session.get('cap_battle') - self.start_session.get('cap_battle')
		decap_battle_gain = current_session.get('decap_battle') - self.start_session.get('decap_battle')

		#Usable Values
		if battles:
			session_winrate = f"{wins / battles * 100:.2f}"

			dmg = f"{dmg_dealt / battles:.0f}"

			kills_per_battle = f"{kills / battles:.2f}"

			spots_per_battle = f"{spots / battles:.2f}"

			dmg_ratio = f"{dmg_dealt / dmg_received:.2f}"


			if deaths:
				kd_ratio = f"{kills / deaths:.2f}"
			else:
				kd_ratio = kills


			self.battlesValue.setText(str(battles))
			self.winrateValue.setText(str(session_winrate))
			self.dmgValue.setText(str(dmg))
			self.drValue.setText(str(dmg_ratio))
			self.kdValue.setText(str(kd_ratio))


app = QApplication(sys.argv)
window = MainWindow()

window.show()
app.exec()