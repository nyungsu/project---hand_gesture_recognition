def judge(system, rps_result):
        # if len(rps_result) >= 2:
        #     winner = None
        #     text = ''
            
        if system==0:
            if rps_result == 0     : text = 'Tie'
            elif rps_result == 3  : text = 'Paper wins'  ; winner = 1
            elif rps_result == 1 or 2: text = 'Rock wins'   ; winner = 0
            
        elif system ==3:
            if rps_result == 0     : text = 'Paper wins'  ; winner = 0
            elif rps_result == 3  : text = 'Tie'
            elif rps_result == 1 or 2: text = 'Scissors wins'; winner = 1
            
        elif system == 1 or system == 2:
            if rps_result == 0     : text = 'Rock wins'   ; winner = 1
            elif rps_result == 3  : text = 'Scissors wins'; winner = 0
            elif rps_result == 1 or 2: text = 'Tie'
        return text, winner
    
    # def drawing_result(winner,img):
        
    #     if winner is not None:
    #         cv2.putText(img, text='Winner', org=(rps_result[winner]['org'][0], rps_result[winner]['org'][1] + 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 255, 0), thickness=3)
    #     cv2.putText(img, text=text, org=(int(img.shape[1] / 2), 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)

# test bench
# [{'rps':  3, 'org': (...)}, {'rps': 'rock', 'org': (...)}]
# test = [{'rps' : 'rock',}, {'rps':  3}]
# text, winner = judge(test)

# print(text, winner)
