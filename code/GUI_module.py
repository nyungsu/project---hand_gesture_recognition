import cv2
import threading
import numpy as np
#QT
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QIcon

from Ui_MainWindow import Ui_MainWindow
from RSPgame_module import RSPgame


running = False
class MainWindow:
    def __init__(self):
        # init
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
       
        # setting
        self.init_img()      
        self.set_btn()    
        
        
        self.RSPmodel = RSPgame()
        self.RSPmodel.making_system_rps()
        
        # cam_run에서 GameMode가 True 일 때만 judge 메소드로 가서 판별하게
        self.GameMode = True
        
        # cam_run에서 GameMode가 True 됐을 때 한 번만 sys 이미지 변경 시킬
        # self.change_sys_img = True
        self.count = 0
        

    def show(self):
        # window icon
        self.main_win.setWindowIcon(QIcon('image/icon1.png'))
        self.main_win.show()

    def init_img(self):
        self.qPixmap = QPixmap()
        self.qPixmap.load("image/snoopy_face.png")
        self.qPixmap = self.qPixmap.scaledToHeight(300)
        self.ui.img_me.setPixmap(self.qPixmap)

        self.qPixmap.load("image/snoopy_user.png")
        self.qPixmap = self.qPixmap.scaledToHeight(300)
        self.ui.img_you.setPixmap(self.qPixmap)
        
    def RSP_img(self):
        # GameMode False 일 때 , 초기 값으로
        if self.GameMode == False:
            self.qPixmap.load("image/snoopy_face.png")
            self.qPixmap = self.qPixmap.scaledToHeight(300)
            self.ui.img_me.setPixmap(self.qPixmap)
            self.count = 0
            
        self.count += 1
        
        
        # init_1
        if self.count < 40:
            self.qPixmap = QPixmap()
            self.qPixmap.load("image/init_1.png")
            self.qPixmap = self.qPixmap.scaledToHeight(300)
            self.ui.img_me.setPixmap(self.qPixmap)
            
        # init_2
        elif self.count >= 40 and self.count < 80:
            self.qPixmap.load("image/init_2.png")
            self.qPixmap = self.qPixmap.scaledToHeight(300)
            self.ui.img_me.setPixmap(self.qPixmap)
        
        # init_3
        elif self.count >= 80 and self.count <110 :
            self.qPixmap.load("image/init_3.png")
            self.qPixmap = self.qPixmap.scaledToHeight(300)
            self.ui.img_me.setPixmap(self.qPixmap)  
            
        elif self.count >=110 :
            if self.RSPmodel.system == 0:
                self.qPixmap.load("image/rock.png")
                self.qPixmap = self.qPixmap.scaledToHeight(300)
                self.ui.img_me.setPixmap(self.qPixmap)
                
            elif self.RSPmodel.system == 1 or self.RSPmodel.system == 3:
                self.qPixmap.load("image/scissors.png")
                self.qPixmap = self.qPixmap.scaledToHeight(300)
                self.ui.img_me.setPixmap(self.qPixmap)
                
            elif self.RSPmodel.system == 2:
                self.qPixmap.load("image/paper.png")
                self.qPixmap = self.qPixmap.scaledToHeight(300)
                self.ui.img_me.setPixmap(self.qPixmap)
        
        

    def set_btn(self): 
        self.ui.btn_start.clicked.connect(self.cam_start)
        self.ui.btn_stop.clicked.connect(self.cam_stop)
        
    def cam_run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        while running:  
            ret, img = cap.read()
            if ret:
                if self.GameMode == True:
                    
                    self.RSP_img()
                    # print(self.RSPmodel.text)
                    # self.RSPmodel.text로 결과 받을 수 있음
                    if self.count >=110 and self.count <=130:
                        self.RSPmodel.judge(img)
                    
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.flip(img, 1)
                
                # flip 밑에 넣어야 글자 안 뒤집히더라
                if self.RSPmodel.text != None:
                    cv2.putText(img, text=self.RSPmodel.text,
                                org=(int(img.shape[1] / 2), 100),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=2, color=(0, 0, 255),
                                thickness=3)
                    
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

    
