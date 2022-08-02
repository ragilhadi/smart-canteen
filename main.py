from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
import cv2 as cv
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
from utils.faciallandmark import FacialLandmark


fl = FacialLandmark()
color = {
    "primary":'#479F91', 
    "secondary":'#F3DB2B',
    "background":'#F3FEDC'
    }

food_menus = ['Nasi Doang', 'Nasi Garem', 'Nasi Pilus', 'Nasi Campur', 'Nasi Kuli', 'Pecel Ayam']

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("FacialLandmark ft Optical Flow - SmartCanteen.mp3")
        MainWindow.resize(1920, 980)
        MainWindow.setStyleSheet(f"background-color: {color['background']};")
        self.app_name = 'FacialLandmark ft Optical Flow - SmartCanteen.mp3'
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Gloal Variable
        self.pick_menu = False
        self.confirm_menu = False
        self.picked = -1
        self.message = 'Silahkan menghadapkan wajah pada kamera'
        self.command = 0

        ## Image UI
        self.filkom_img = QtWidgets.QLabel(self.centralwidget)
        self.filkom_img.setGeometry(QtCore.QRect(30, 20, 291, 91))
        self.filkom_img.setText("")
        self.filkom_img.setPixmap(QtGui.QPixmap("assets/filkom.png"))
        self.filkom_img.setScaledContents(True)
        self.filkom_img.setObjectName("filkom_img")
        self.hint_img = QtWidgets.QLabel(self.centralwidget)
        self.hint_img.setGeometry(QtCore.QRect(720, 860, 561, 91))
        self.hint_img.setText("")
        self.hint_img.setPixmap(QtGui.QPixmap("assets/hint.png"))
        self.hint_img.setScaledContents(True)
        self.hint_img.setObjectName("hint_img")

        ## Camera and Button UI
        self.camera = QtWidgets.QLabel(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(1620, 20, 271, 231))
        self.camera.setStyleSheet(" border: 5px solid black;")
        self.camera.setText("")
        self.camera.setScaledContents(True)
        self.camera.setObjectName("camera")
        self.camera.setPixmap(QtGui.QPixmap("assets/no_camera.png"))
        self.camera_btn = QtWidgets.QPushButton(self.centralwidget)
        self.camera_btn.setGeometry(QtCore.QRect(1620, 270, 271, 51))
        self.camera_btn.setObjectName("camera_btn")
        self.camera_btn.setText("Start")
        self.camera_btn.setStyleSheet(f"background-color: {color['secondary']}; border-radius: 20")

        ## Dummy Button
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(1320, 270, 271, 51))
        self.next.setObjectName("next")
        self.next.setText("Next")
        self.next.clicked.connect(lambda: self.change_cursor(1))
        self.next.setStyleSheet(f"color: white; background-color: {color['primary']}; border-radius: 20")
        self.prev = QtWidgets.QPushButton(self.centralwidget)
        self.prev.setGeometry(QtCore.QRect(1030, 270, 271, 51))
        self.prev.setObjectName("prev")
        self.prev.setText("Prev")
        self.prev.clicked.connect(lambda: self.change_cursor(-1))
        self.prev.setStyleSheet(f"color: white; background-color: {color['primary']}; border-radius: 20")

        # Design Ornament
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(630, 30, 511, 141))
        font_title = QtGui.QFont()
        font_title.setPointSize(39)
        self.title.setFont(font_title)
        self.title.setTextFormat(QtCore.Qt.PlainText)
        self.title.setScaledContents(True)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.title.setText("SMART CANTEEN")
        self.title.setStyleSheet(f"color: {color['primary']};")

        ## Message Dialog
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(40, 250, 511, 71))
        font_message = QtGui.QFont()
        font_message.setPointSize(20)
        self.message.setFont(font_message)
        self.message.setTextFormat(QtCore.Qt.PlainText)
        self.message.setScaledContents(True)
        self.message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.message.setObjectName("message")
        self.message.setText("Hidupkan Kamera")

        ## Food Menus UI
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 340, 1861, 301))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        font_food = QtGui.QFont()
        font_food.setPointSize(24)
        self.food_0 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.food_0.setAlignment(QtCore.Qt.AlignCenter)
        self.food_0.setObjectName("food_0")
        self.food_0.setText("Nasi Doang")
        self.food_0.setFont(font_food)
        self.food_0.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.horizontalLayout.addWidget(self.food_0)
        self.food_1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.food_1.setAlignment(QtCore.Qt.AlignCenter)
        self.food_1.setObjectName("food_1")
        self.food_1.setText("Nasi Garem")
        self.food_1.setFont(font_food)
        self.food_1.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.horizontalLayout.addWidget(self.food_1)
        self.food_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.food_2.setAlignment(QtCore.Qt.AlignCenter)
        self.food_2.setObjectName("food_2")
        self.food_2.setText("Nasi + Pilus")
        self.food_2.setFont(font_food)
        self.food_2.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.horizontalLayout.addWidget(self.food_2)
        self.food_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.food_3.setAlignment(QtCore.Qt.AlignCenter)
        self.food_3.setObjectName("food_3")
        self.food_3.setText("Nasi Campur")
        self.food_3.setFont(font_food)
        self.food_3.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.horizontalLayout.addWidget(self.food_3)
        self.food_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.food_4.setAlignment(QtCore.Qt.AlignCenter)
        self.food_4.setObjectName("food_4")
        self.food_4.setText("Nasi Kuli")
        self.food_4.setFont(font_food)
        self.food_4.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.horizontalLayout.addWidget(self.food_4)
        self.food_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.food_5.setAlignment(QtCore.Qt.AlignCenter)
        self.food_5.setObjectName("food_9")
        self.food_5.setText("Pecel Ayam")
        self.food_5.setFont(font_food)
        self.food_5.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.horizontalLayout.addWidget(self.food_5)
        self.pick_img = QtWidgets.QLabel(self.centralwidget)
        self.pick_img.setGeometry(QtCore.QRect(40, 650, 1851, 61))
        font_hint = QtGui.QFont()
        font_hint.setPointSize(16)
        self.pick_img.setFont(font_hint)
        self.pick_img.setAlignment(QtCore.Qt.AlignCenter)
        self.pick_img.setObjectName("pick_img")
        self.pick_img.setText("PILIH ⬇️")
        self.pick_img.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.food_picked = QtWidgets.QLabel(self.centralwidget)
        self.food_picked.setGeometry(QtCore.QRect(50, 740, 591, 71))
        font_food_picked = QtGui.QFont()
        font_food_picked.setPointSize(18)
        self.food_picked.setFont(font_food_picked)
        self.food_picked.setObjectName("food_picked")
        self.food_picked.setText("Makanan yang dipilih : -")
        self.food_picked.setStyleSheet(f"color: {color['primary']};")
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.camera_btn.clicked.connect(self.controlTimer)
        self.cursor_highlight()


    def viewCam(self):
        ret, image = self.cap.read()
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.flip(image, 1)
        image, message_text, self.command = fl.detection(image)
        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        if self.pick_menu:
            self.change_cursor(self.command)
        
        self.camera.setPixmap(QPixmap.fromImage(qImg))
        self.pick_highlight(self.command)
        self.message.setText(message_text)

    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv.VideoCapture(0)
            self.timer.start(20)
            self.camera_btn.setText("Stop")
        else:
            self.timer.stop()
            self.cap.release()
            self.camera.setPixmap(QtGui.QPixmap("assets/no_camera.png"))
            self.camera_btn.setText("Start")
            self.message.setText("Hidupkan Kamera")

    def change_cursor(self, step):
        if self.picked == 0:
            if step < 0:
                self.picked = 0
            else:
                self.picked += step
                self.cursor_highlight()

        else:
            self.picked += step
            self.cursor_highlight()

    def start_pick(self):
        if self.pick_menu:
            pass

    def reset_cursor(self):
        self.food_0.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.food_1.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.food_2.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.food_3.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.food_4.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        self.food_5.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        

    def cursor_highlight(self):
        if self.picked == -1:
            self.reset_cursor()

        if self.picked == 0:
            self.reset_cursor()
            self.food_0.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
            self.food_picked.setText(f"Makanan yang dipilih : {food_menus[0]}")

        elif self.picked == 1:
            self.reset_cursor()
            self.food_1.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
            self.food_picked.setText(f"Makanan yang dipilih : {food_menus[1]}")

        elif self.picked == 2:
            self.reset_cursor()
            self.food_2.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
            self.food_picked.setText(f"Makanan yang dipilih : {food_menus[2]}")

        elif self.picked == 3:
            self.reset_cursor()
            self.food_3.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
            self.food_picked.setText(f"Makanan yang dipilih : {food_menus[3]}")

        elif self.picked == 4:
            self.reset_cursor()
            self.food_4.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
            self.food_picked.setText(f"Makanan yang dipilih : {food_menus[4]}")

        elif self.picked == 5:
            self.reset_cursor()
            self.food_5.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
            self.food_picked.setText(f"Makanan yang dipilih : {food_menus[5]}")

    def pick_highlight(self, command):
        if command == -10: # Face up
            self.pick_menu = False
            self.picked = -1
            self.pick_img.setStyleSheet(f"color: {color['secondary']}; background-color: {color['primary']}; border-radius: 20; font-weight: bold")
        elif command == 10: # Face down
            self.pick_menu = True
            self.picked = 0
            # self.pick_img.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")
        elif command == 20: # Face down
            self.pick_menu = False
            self.pick_img.setStyleSheet(f"color: {color['primary']}; background-color: {color['secondary']}; border-radius: 20; font-weight: bold")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(self.app_name, self.app_name))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

