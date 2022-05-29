import cv2
import mediapipe as mp
import numpy as np
import random

class RSPgame():
    def __init__(self) -> None:
        self.rps_gesture = {0:'rock', 1:'scissors', 2:'paper', 3:'scissors'}
        self.max_num_hands = 1
        # mediapipe init
        # 메모리에 계속 올리고 있어야 해서 init 함수 o
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_num_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.system = None
        self.winner = None
        self.text = None
        self.KNN_init()

    def KNN_init(self):
        # 제스쳐 인식할 때 사용할 KNN 모델 선언
        # knn 모델은 한 번 만 선언 하면 되기 때문에 init 함수 안 하고 따로 선언
        file = np.genfromtxt('data/gesture_train.csv', delimiter=',')
        angle = file[:,:-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        self.knn = cv2.ml.KNearest_create()
        self.knn.train(angle, cv2.ml.ROW_SAMPLE, label)

    def making_system_rps(self):
        # 가위바위보 system 묵찌빠임
        self.system = random.randint(0,3)          
        print(self.system)

    def judge(self,img):
        result = self.hands.process(img)                                                        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  

        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 3))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z]

                # 특징점 벡터 계산
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
                v = v2 - v1 # [20,3]
                # 벡터 정규화
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # 내적한 결과를 아크 코싸인에 넣어서 각도 구함
                angle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                    v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

                # 라디안을 degree로
                angle = np.degrees(angle) 
                
                # Inference gesture
                data = np.array([angle], dtype=np.float32)
                _, results, _, _ = self.knn.findNearest(data, 3)
                rps_result = int(results[0][0])                                    # 여기에 인식한 가위바위보 dict key 형태 저장 됨
                
                
                # {0:'rock', 1:'12scissors', 2:'paper', 3:'23-scissors'}
                if self.system==0:
                    if rps_result == 0     : self.text = 'Tie'
                    elif rps_result == 2  : self.text = 'User wins'
                    elif rps_result == 1 or 3: self.text = 'Sys wins'   
        
                elif self.system ==2:
                    if rps_result == 0     : self.text = 'Sys wins'  
                    elif rps_result == 2  : self.text = 'Tie'
                    elif rps_result == 1 or 3: self.text = 'User wins'
                    
                elif self.system == 1 or self.system == 3:
                    if rps_result == 0     : self.text = 'User wins'
                    elif rps_result == 2  : self.text = 'Sys wins'
                    elif rps_result == 1 or 3: self.text = 'Tie'
                    
            
                
           
            
            
            
            

        