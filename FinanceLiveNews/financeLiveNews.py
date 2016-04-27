import sys
import time,threading
import sched,winsound
import re
import requests
from financeLiveNewsDialog import Ui_Dialog
from PyQt5.QtWidgets import QApplication,QDialog

global schedule
global isAutoRefresh
global lastTime
global ui

schedule = sched.scheduler(time.time, time.sleep)
isAutoRefresh = True
lastTime = ''

def ShowLiveNews():
	global lastTime

	html = requests.get("http://kuaixun.eastmoney.com/")
	divs = re.findall('<div id="livenews-id-(.*?)</div>',html.text,re.S)
	livenewsNum = 0
	list = []
	divIndex = 0
	for div in divs:
		livenewsTime = re.findall('<span class="time">(.*?)</span>',div,re.S)
		livenewsContent = re.findall('class="media-title">(.*?)<',div,re.S)
		if len(livenewsTime) == 0 or len(livenewsContent) == 0:
			return []

		strNews = livenewsTime[0]+livenewsContent[0]
		print(strNews)
		list.append(strNews)
		livenewsNum = livenewsNum + 1

		if divIndex == 0:
			if lastTime != livenewsTime[0]:
				lastTime = livenewsTime[0]
			else:
				return []
		divIndex = divIndex + 1

		if(livenewsNum >= 30):
			break
	return list

def perform_command(inc):
	global schedule

	schedule.enter(inc, 0, perform_command, (inc,))
	if isAutoRefresh == True:
		onNewsRefresh()

def timming_exe(inc = 60):
	global schedule

	schedule.enter(inc, 0, perform_command, (inc,))
	schedule.run()

def loop():
	timming_exe(10)

def addThread():
	t = threading.Thread(target = loop)
	t.setDaemon(True)
	t.start()

def onNewsRefresh():
	global ui

	list = ShowLiveNews()
	if len(list) == 0:
		return

	ui.listWidget.clear()
	for item in list:
		ui.listWidget.addItem(item+'\n')

	winsound.PlaySound('complete',winsound.SND_ALIAS)

def changeAutoRefresh(int):
	print(int)
	global isAutoRefresh
	if int == 0:
		isAutoRefresh = False
	else:
		isAutoRefresh = True

def onHandRefresh(evt):
	onNewsRefresh()

def initEvents():
	global ui
	ui.checkBox.stateChanged['int'].connect(changeAutoRefresh)
	ui.pushButton.clicked.connect(onHandRefresh)

if __name__ == '__main__':
	global ui
	app = QApplication(sys.argv)
	window = QDialog()
	ui = Ui_Dialog()
	ui.setupUi(window)
	initEvents()

	onNewsRefresh()
	addThread()

	window.show()
	sys.exit(app.exec_())