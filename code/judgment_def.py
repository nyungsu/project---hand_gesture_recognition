def judge(rps_result):
        if len(rps_result) >= 2:
            winner = None
            text = ''
            
            if rps_result[0]['rps']=='rock':
                if rps_result[1]['rps']=='rock'     : text = 'Tie'
                elif rps_result[1]['rps']=='paper'  : text = 'Paper wins'  ; winner = 1
                elif rps_result[1]['rps']=='scissors': text = 'Rock wins'   ; winner = 0
            elif rps_result[0]['rps']=='paper':
                if rps_result[1]['rps']=='rock'     : text = 'Paper wins'  ; winner = 0
                elif rps_result[1]['rps']=='paper'  : text = 'Tie'
                elif rps_result[1]['rps']=='scissors': text = 'Scissors wins'; winner = 1
            elif rps_result[0]['rps']=='scissors':
                if rps_result[1]['rps']=='rock'     : text = 'Rock wins'   ; winner = 1
                elif rps_result[1]['rps']=='paper'  : text = 'Scissors wins'; winner = 0
                elif rps_result[1]['rps']=='scissors': text = 'Tie'
        return text, winner
    
    # def drawing_result(winner,img):
        
    #     if winner is not None:
    #         cv2.putText(img, text='Winner', org=(rps_result[winner]['org'][0], rps_result[winner]['org'][1] + 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 255, 0), thickness=3)
    #     cv2.putText(img, text=text, org=(int(img.shape[1] / 2), 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)

# test bench
[{'rps': 'paper', 'org': (...)}, {'rps': 'rock', 'org': (...)}]
test = [{'rps' : 'rock',}, {'rps': 'paper'}]
text, winner = judge(test)

print(text, winner)
