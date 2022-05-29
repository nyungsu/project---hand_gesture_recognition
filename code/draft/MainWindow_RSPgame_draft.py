import sys
import random as rd
import prince
import math
import cv2
import threading
#QT
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidget, QVBoxLayout, QTableWidgetItem, QMessageBox
from PyQt5.QtWidgets import QGraphicsOpacityEffect 
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QPainter
# from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from Ui_MainWindow import Ui_MainWindow

running = False
class MainWindow:
    def __init__(self):
        #기본셋팅
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        #sns.set_style("whitegrid")
        
        #setting
        self.set_img()      
        self.set_btn()      

    def show(self):
        #window icon
        self.main_win.setWindowIcon(QIcon('icon1.png'))
        self.main_win.show()

        
    #set_ : 초기 셋팅    
    def set_img(self): #이미지 셋팅 예시
        self.qPixmap = QPixmap()
        self.qPixmap.load("snoopy_face.png")
        self.qPixmap = self.qPixmap.scaledToHeight(300)
        self.ui.img_me.setPixmap(self.qPixmap)

        self.qPixmap.load("snoopy_user.png")
        self.qPixmap = self.qPixmap.scaledToHeight(300)
        self.ui.img_you.setPixmap(self.qPixmap)

    def set_btn(self): 
        self.ui.btn_start.clicked.connect(self.cam_start)
        self.ui.btn_stop.clicked.connect(self.cam_stop)
        
    def cam_run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while running:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.ui.img_you.setPixmap(pixmap)
                
            else:
                QtWidgets.QMessageBox.about(self.main_win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
        cv2.destroyAllWindows()
        
    def cam_start(self):
        global running
        running = True
        th = threading.Thread(target=self.cam_run)
        th.start()
        print("started..")

    def cam_stop(self):
        global running
        running = False
        print("stoped..")
        self.set_img()   
    

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
    
