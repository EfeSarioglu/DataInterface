from PyQt5.QtWidgets import*
import random
import sys
from designer import Ui_MainWindow
from datetime import datetime
from matplotlib import dates as mpl_dates
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap,QIcon

class dataIterface(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.data = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ";35;39°46'50\";N; 32°48'15\";E;180°;%14"
        self.datas = self.data.split(";")
        self.ui.dateEdit.setDate(datetime.now())
        self.setFixedSize(1000,500)
        self.setWindowIcon(QIcon("images/icon.png"))
        

        self.dates = [datetime.strptime(datetime.strftime(datetime.strptime(self.datas[0],"%Y-%m-%d %H:%M:%S"),"%H:%M:%S"),"%H:%M:%S")]
        self.temp = [int(self.datas[1])]
        self.lineColor = 'blue'

        self.ui.dataGraph.canvas.axes.set_position([0.15,0.30,0.75,0.55])

        self.refleshBoard()

        self.timer = QTimer()
        self.chargeTimer = QTimer()
        self.timer.timeout.connect(self.updateData)
        self.chargeTimer.timeout.connect(self.reduceCharge)
        self.timer.start(2000)
        self.chargeTimer.start(10000)

    def updateData(self):
        self.datas[0] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.datas[1] = str(random.randint(10,50))
        self.datas[2] = self.datas[2][:-3] + str(random.randint(10,59)) +"\""
        self.datas[4] = self.datas[4][:-3] + str(random.randint(10,59)) +"\""
        self.datas[6] = str(random.randint(0,359)) + "°"
        self.dates.append(datetime.strptime(datetime.strftime(datetime.strptime(self.datas[0],"%Y-%m-%d %H:%M:%S"),"%H:%M:%S"),"%H:%M:%S"))
        self.temp.append(int(self.datas[1]))

        self.checkWarning()
        self.refleshBoard()

    def reduceCharge(self):
        self.datas[7] = "%" + str(int(self.datas[7][1:]) -1)

    def refleshBoard(self):
        self.ui.LocationD.setText(self.datas[2]+self.datas[3]+self.datas[4]+self.datas[5])
        self.ui.AngleD.setText(self.datas[6])
        self.ui.tempD.setText(self.datas[1])
        self.ui.ChargeD.setText(self.datas[7])
        self.ui.dataGraph.canvas.axes.clear()
        for label in self.ui.dataGraph.canvas.axes.get_xticklabels():
            label.set_rotation(90)
        self.ui.dataGraph.canvas.axes.xaxis.set_major_formatter(mpl_dates.DateFormatter("%H:%M:%S"))
        self.ui.dataGraph.canvas.axes.plot_date(self.dates,self.temp,linestyle='solid',color=self.lineColor,marker=',')
        self.ui.dataGraph.canvas.axes.set_title('Sıcaklık/Zaman Grafiği')
        self.ui.dataGraph.canvas.axes.set_xlabel("zaman")
        self.ui.dataGraph.canvas.axes.set_ylabel("sıcaklık (°C)")
        self.ui.dataGraph.canvas.draw()

    def checkWarning(self):

        if int(self.datas[1])>=45 and int(self.datas[7][1:])<10:
            self.ui.warningSign.setPixmap(QPixmap("images/signWarnK.png"))
            self.lineColor = 'red'
            self.ui.tempD.setStyleSheet("color: rgb(170, 0, 0)")
            self.ui.ChargeD.setStyleSheet("color: rgb(170, 0, 0)")
            self.ui.warningSign.setToolTip("Sıcaklık 45 Derecenin Üstünde!\nŞarj Seviyesi 10'un Altında!")
        elif int(self.datas[1])>=45 and int(self.datas[7][1:])>=10:
            self.ui.warningSign.setPixmap(QPixmap("images/signWarnK.png"))
            self.lineColor = 'red'
            self.ui.tempD.setStyleSheet("color: rgb(170, 0, 0)")
            self.ui.ChargeD.setStyleSheet("color: rgb(0, 0, 0)")
            self.ui.warningSign.setToolTip("Sıcaklık 45 Derecenin Üstünde!")
        elif int(self.datas[1])<45 and int(self.datas[7][1:])<10:
            self.ui.warningSign.setPixmap(QPixmap("images/signWarnK.png"))
            self.lineColor = 'blue'
            self.ui.tempD.setStyleSheet("color: rgb(0, 0, 0)")
            self.ui.ChargeD.setStyleSheet("color: rgb(170, 0, 0)")
            self.ui.warningSign.setToolTip("Şarj Seviyesi 10'un Altında!")
        else:
            self.ui.warningSign.setPixmap(QPixmap("images/signWarnY.png"))
            self.lineColor = 'blue'
            self.ui.tempD.setStyleSheet("color: rgb(0, 0, 0)")
            self.ui.ChargeD.setStyleSheet("color: rgb(0, 0, 0)")
            self.ui.warningSign.setToolTip("Sorun Yok!")

app = QApplication(sys.argv)
win = dataIterface()
win.show()
sys.exit(app.exec_())