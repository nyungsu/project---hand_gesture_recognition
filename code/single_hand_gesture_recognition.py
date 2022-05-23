import timeit
import cv2
import mediapipe as mp
import numpy as np

max_num_hands = 1
rps_gesture = {0:'rock', 1:'scissors', 2:'scissors', 3:'paper'}

# MediaPipe hands 모델 선언
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=max_num_hands,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# 제스쳐 인식할 때 사용할 KNN 모델 선언
file = np.genfromtxt('data/gesture_train.csv', delimiter=',')
angle = file[:,:-1].astype(np.float32)
label = file[:, -1].astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)

cap = cv2.VideoCapture(0)

frame_cnt = 0
system = 1          # 가위바위보 system 묵찌빠임 랜덤함수 넣어서 랜덤하게 바뀌게 해야함

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue
    
    start_time = timeit.default_timer()         # fps 측정용 타이머 시작
    
    img = cv2.flip(img, 1)                      # 영상 좌우 대칭
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(img)                 # OpenCV는 BGR순, MP는 RGB순
                                                # 선언한 모델에 RGB 순으로 영상 입력

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 출력을 위해 다시 OpenCV BGR순으로 변경

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
            ret, results, neighbours, dist = knn.findNearest(data, 3)
            rps_result = int(results[0][0])                                    # 여기에 인식한 가위바위보 dict key 형태 저장 됨
            
            winner = None
            if system==0:
                if rps_result == 0     : text = 'Tie'
                elif rps_result == 3  : text = 'User wins'  ; winner = 1
                elif rps_result == 1 or 2: text = 'System wins'   ; winner = 0
            
            elif system ==3:
                if rps_result == 0     : text = 'System wins'  ; winner = 0
                elif rps_result == 3  : text = 'Tie'
                elif rps_result == 1 or 2: text = 'User wins'; winner = 1
                
            elif system == 1 or system == 2:
                if rps_result == 0     : text = 'User wins'   ; winner = 1
                elif rps_result == 3  : text = 'System wins'; winner = 0
                elif rps_result == 1 or 2: text = 'Tie'
                
            org = (int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0]))    # putText 위치 좌표
            cv2.putText(img, text=text, org=(int(img.shape[1] / 2), 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3) # 화면에 승패 글자 출력





            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
            
    terminate_time = timeit.default_timer()             # fps 측정용 타이머 종료
    
    ## 누적 프레임 출력 코드 (사용해보니까 많이느리네)
    # FPS = int(1./(terminate_time - start_time ))
    # if ret:
    #     frame_cnt += 1
    
    # FPS += FPS/frame_cnt
    # print(FPS)    
    
    
    cv2.imshow('Game', img)
    if cv2.waitKey(1) == ord('q'):
        break

