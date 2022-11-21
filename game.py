import cv2
import mediapipe as mp
import random
import datetime
import sqlite3
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cam_width = 640
cam_height = 480

#webcam input
cap = cv2.VideoCapture(0)
#webcam setting 
cap.set(cv2.CAP_PROP_FRAME_WIDTH,cam_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,cam_height)
cap.set(cv2.CAP_PROP_FPS,30)

#DBファイル存在フラグ
isFileExists = False

if os.path.exists("score.sqlite3"):
    isFileExists = True

#sqlite3接続(DBファイル生成)
con = sqlite3.connect("score.sqlite3")
#sqliteカーソル取得
cur = con.cursor()

if isFileExists == False :
    #DBファイルが存在しないとき
    #テーブル作成
    cur.execute("create table score_table(date text,score real);")
    con.commit()

while True:

    #的の座標を格納するための配列
    circle = []
    #的の個数
    circle_count = 10
    #的の半径
    circle_radius = 25
    #的の表示管理の配列
    circle_display = [True] * circle_count
    #次に消す的
    circle_next_id = 0

    #シーン
    scene = 0

    #座標重複検査のための配列
    circle_x_tmp = []
    circle_y_tmp = []

    #タイムスタンプ関連の処理フラグ
    isReady = False
    #タイムスタンプ格納変数の初期化
    start_time =  datetime.timedelta(seconds=0)
    end_time =  datetime.timedelta(seconds=0)

    #ゲーム時間(s)
    game_time = 25
    #クリアタイム
    clear_time = str(game_time)

    #ゲームクリアフラグ
    isClear = False

    #的の座標を生成
    while len(circle) < circle_count:
        circle_x = random.randrange(20,cam_width-20,25)
        circle_y = random.randrange(20,cam_height-20,25)
        if (not circle_x in circle_x_tmp) & (not circle_y in circle_y_tmp):
            circle_x_tmp.append(circle_x)
            circle_y_tmp.append(circle_y)
            circle.append([circle_x,circle_y])

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        #メインループ
        while cap.isOpened():

            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if scene == 0:
                #タイトル画面

                #スタートボタン位置
                start_btn_1 = (cam_width//2 - 150,cam_height//2 + 120)
                start_btn_2 = (cam_width//2+150 ,cam_height//2 + 170)


                #手を認識したときに赤丸を描画する
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand_x = int(hand_landmarks.landmark[9].x * cam_width)
                        hand_y = int(hand_landmarks.landmark[9].y * cam_height)
                        cv2.circle(image,(hand_x,hand_y),10,color=(0,0,255),thickness=-1)


                        if (start_btn_1[0] <  (cam_width - hand_x)) & (start_btn_2[0] > (cam_width - hand_x)):
                                if(start_btn_1[1] < hand_y) & (start_btn_2[1] >  hand_y):
                                    #カウントダウンへ遷移
                                    scene = 1

                #カメラ画像反転
                image = cv2.flip(image, 1)


                #タイトル表示
                cv2.putText(image,"Catch Game",(cam_width//2 - 290,cam_height//2),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),4,cv2.LINE_AA)   
                #スタートボタン表示
                cv2.rectangle(image,start_btn_1,start_btn_2,(255,255,255),thickness=-1) 
                cv2.putText(image,"Touch to Start",(cam_width//2 - 140,cam_height//2+160),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,255),4,cv2.LINE_AA)   

            elif scene == 1:
                #カウントダウン
                if isReady == False:
                    start_time = datetime.datetime.now() + datetime.timedelta(seconds=4)
                    isReady = True
                if((start_time - datetime.datetime.now()).seconds == 0):
                    #ゲーム本体へ遷移
                    scene = 2
                    isReady = False

                #手を認識したときに赤丸を描画する
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand_x = int(hand_landmarks.landmark[9].x * cam_width)
                        hand_y = int(hand_landmarks.landmark[9].y * cam_height)
                        
                        cv2.circle(image,(hand_x,hand_y),10,color=(0,0,255),thickness=-1)

                #カメラ画像反転
                image = cv2.flip(image, 1) 

                cv2.putText(image,str((start_time - datetime.datetime.now()).seconds),(cam_width//2 - 20,cam_height//2-10),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,255),4,cv2.LINE_AA)

            elif scene == 2:
                #ゲーム本体

                #カウントダウン
                if isReady == False:
                    end_time = datetime.datetime.now() + datetime.timedelta(seconds=game_time)
                    isReady = True


                #手を認識したときに赤丸を描画する
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand_x = int(hand_landmarks.landmark[9].x * cam_width)
                        hand_y = int(hand_landmarks.landmark[9].y * cam_height)
                        
                        cv2.circle(image,(hand_x,hand_y),10,color=(0,0,255),thickness=-1)

                        #手と的の衝突判定
                        for i in range(circle_count):
                            if ((circle[i][0] - circle_radius) <  (cam_width - hand_x)) & ((circle[i][0] + circle_radius) > (cam_width - hand_x)):
                                if((circle[i][1] - circle_radius ) < hand_y) & ((circle[i][1] + circle_radius) >  hand_y):
                                    if circle_next_id == i :
                                        circle_display[i] = False
                                        circle_next_id += 1

                #ゲームクリア判定
                if circle_next_id == circle_count:
                    #ゲーム終了へ遷移
                    clear_time = (end_time - datetime.datetime.now()).total_seconds()
                    
                    isClear = True
                    isReady = False
                    scene = 3

                #ゲームオーバー判定
                if((end_time - datetime.datetime.now()).seconds == 0):
                    #ゲーム終了へ遷移
                    scene = 3
                    #isReady = False

                #print(circle)

                #カメラ画像反転
                image = cv2.flip(image, 1) 

                #的を描画する
                for i in range(circle_count):
                    if circle_display[i] == True:
                        cv2.circle(image,(circle[i][0],circle[i][1]),circle_radius,color=(255,0,0),thickness=-1)
                        cv2.putText(image,str(i+1),(circle[i][0]-13,circle[i][1]+10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2,cv2.LINE_AA)
                #秒数表示
                cv2.putText(image,str((end_time - datetime.datetime.now()).seconds),(cam_width//2 - 40,cam_height//2-10),cv2.FONT_HERSHEY_SIMPLEX,3,(0,255,255),4,cv2.LINE_AA)
            
                

            elif scene == 3:
                #ゲーム終了
                #手を認識したときに赤丸を描画する
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand_x = int(hand_landmarks.landmark[9].x * cam_width)
                        hand_y = int(hand_landmarks.landmark[9].y * cam_height)
                        cv2.circle(image,(hand_x,hand_y),10,color=(0,0,255),thickness=-1)
                #カメラ画像反転
                image = cv2.flip(image, 1)
                if isClear == True:
                    #ゲームクリア表示
                    cv2.putText(image,"GAME CLEAR!!",(cam_width//2 - 320,cam_height//2),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4,cv2.LINE_AA)
                    cv2.putText(image,str("Clear Time: "+str(clear_time)),(cam_width//2 - 220,cam_height//2 + 100),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,255),2,cv2.LINE_AA)
                    if isReady == False:
                        play_date = str(datetime.datetime.now())
                        cur.execute("insert into score_table(date,score) values (?,?);",(play_date,clear_time))
                        con.commit()
                        isReady = True
                        
                else:
                    #ゲームオーバー表示
                    cv2.putText(image,"GAME OVER",(cam_width//2 - 270,cam_height//2),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),4,cv2.LINE_AA)
         
            cv2.imshow('Catch Game', image)
            keycode = cv2.waitKey(5)
            if keycode & 0xFF == 27:
                #escキーでゲームリセット
                break
            elif keycode & 0xFF == 113:
                #qキーでプロセス終了
                con.close()
                cap.release()
                exit()
con.close()
cap.release()
