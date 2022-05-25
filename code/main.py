from RSPgame import RSPgame

'''
1. model = RSPgame() : 가위 바위 보 모델을 선언해줍니다
                       mediapipe.hands 모델만 선언 됩니다.
                       
2. model.KNN_init() : 선언한 모델에서 KNN_init() 메소드를 실행합니다.
                      학습된 KNN 모델은 가위 바위 보를 판별 하기 전에만 메모리에 올라가면 되기 때문에
                      RSPgame 모델을 선언 할 때 초기 값으로 선언 되지 않게 따로 메소드로 빼서 구현했습니다.
                      
3. model.making_system_rps() : 시스템의 가위 바위 보를 랜덤으로 변수에 넣습니다.
                               시스템이 무엇을 냈는지 확인하기 위해
                               {0:'rock', 1:'12scissors', 2:'paper', 3:'23-scissors'} 에 기반하여
                               임시로 0,1,2,3을 출력하게 해놨습니다.

4. result = model.game() : 가위 바위 보 게임을 시작합니다.
                           q를 누를 경우 게임이 종료 되고, 게임 결과를 result로 받습니다.
'''

model = RSPgame()
model.KNN_init()
model.making_system_rps()
result = model.game()

print(result)
# {0:'rock', 1:'12scissors', 2:'paper', 3:'23-scissors'}