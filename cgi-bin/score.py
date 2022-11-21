#!/usr/bin/python3
import sqlite3
import os

if not os.path.exists("score.sqlite3"):
    #DBファイルが存在しないとき
    #score.sqlite3ファイルを作成
    con = sqlite3.connect("score.sqlite3")
    #sqliteカーソル取得
    cur = con.cursor()
    #テーブル作成
    cur.execute("create table score_table(date text,score real);")
    con.commit()
else:
    #DBファイルが存在するとき
    #sqlite3接続
    con = sqlite3.connect("score.sqlite3")
    #sqliteカーソル取得
    cur = con.cursor()

print("Content-Type: text/html\n\n")

print("<!DOCTYPE html>")
print("<html>")

print("<head>")
print("<meta charset='utf-8'>")
print("<meta http-equiv='refresh' content='10; URL='>")
print("<title>score一覧</title>")
print("</head>")

print("<body>")
print("<h1>score一覧</h1>")
cur.execute("select * from score_table order by score desc;")
score = cur.fetchall()

print("<table border=1 style='text-align:center'>")
print("<tr><th>順位</th><th>日時</th><th>クリア残り時間</th></tr>")
for s in range(len(score)):
    print("<tr>")
    print("<td>")
    print(s+1)
    print("</td>")
    print("<td>")
    print(score[s][0])
    print("</td>")
    print("<td>")
    print(score[s][1])
    print("</td>")
    print("</tr>")   
print("</table>")


print("</body>")

print("</html>")

con.close()
