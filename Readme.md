# Catch Game
## 説明
Webカメラで認識した手のひらで数字の書かれている的をその数字の順番通りにキャッチしていくゲーム 

## 準備

- sqlite3のインストール
```bash
$ sudo apt install sqlite3
```

- mediapipeのインストール
```bash
$ sudo pip install mediapipe
```

## 起動方法
-  ゲーム本体
```bash
$ python3 game.py
```

- スコアボード
```
$ ./server_run.sh
```

## スコアボードへのアクセス
http://localhost:8080/cgi-bin/score.py

## キー割り当て

- ゲームリセット  
Escキー

- プロセス終了  
qキー

## ゲーム説明
1. 手を認識すると赤丸が表示される
2. 赤丸を「Touch to Start」に合わせる
3. カウントダウンが始まり，ゲームが開始する
4. 1～10までの的が表示される
5. 的は手に表示されている赤丸と重なると消える(1から順番に消していく)
6. 制限時間内に全ての的を消すとゲームクリア
7. ゲームクリアするとClear Time(ゲームクリア時点の残り時間)が表示，記録される(スコアボードにも表示される)

