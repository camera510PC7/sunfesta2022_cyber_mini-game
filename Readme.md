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



