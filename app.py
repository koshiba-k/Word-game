import tkinter as tk 
from tkinter import ttk
import random, time, math
import sqlite3

def selectb_db():
    order = varrgo.get()

    select_text = "SELECT * FROM score "
    where_text = "WHERE level in "
    where_list = []
    
    if varckb1.get():
        where_list.append("初級")
    if varckb2.get():
        where_list.append("中級")
    if varckb3.get():
        where_list.append("上級")

    select_text += where_text + "('" + "', '".join(where_list) + "')"
    
    user_name = inp_name.get()
    if user_name:
        if where_list:
            select_text += "AND "
        else:
            select_text += "WHERE "
        select_text += "name LIKE '%" + user_name + "%'"

    if order == 1:
        select_text += " ORDER BY id DESC"
    elif order == 2:
        select_text += " ORDER BY id "
    elif order == 3:
        select_text += " ORDER BY time "
    elif order == 4:
        select_text += " ORDER BY time DESC"
    
    # Log.dbを作成する
    # すでに存在していれば、それにアスセスする
    dbname = 'Log.db'
    conn = sqlite3.connect(dbname)
    
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    cur.execute(select_text)

    textwidget["state"] = "normal"#テキストの入力禁止 解除
    textwidget.delete('1.0', tk.END) #text削除
    
    log_inf =""
    
    s = ["NO.:","難易度 : ","Time : ","Name : ","miss : ","ans : "]
    for t in cur:
        for i, value in enumerate(t):
            log_inf += s[i] +str(value) + "   "
        log_inf = log_inf + "\n"
    
    textwidget.insert(tk.END, log_inf)#難易度|時間|名前｜ミス回数|答え 
    textwidget["state"] = "disabled"#テキストの入力禁止
    
    # データベースへコミット。これで変更が反映される。
    cur.close()
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

def register():
    entry.configure(state='readonly')#テキストの入力禁止
    btn_ist_name["state"] = "disable"
    
    if level == 1:
        lev = "初級"
    elif level == 2:
        lev = "中級"
    elif level ==3:
        lev = "上級"
    
    name = entry.get()
    if not name:
        name = "NoName"
    
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    #テーブル作成
    cur.execute("CREATE TABLE IF NOT EXISTS SCORE(id INTEGER PRIMARY KEY AUTOINCREMENT,level,time,name,miss,answer)")
    
    #難易度|時間|名前｜ミス回数|答え insert
    cur.execute('INSERT INTO score(level,time,name,miss,answer) VALUES(?,?,?,?,?)', (lev,time_,name,miss,r))

    conn.commit()  # データベースへの変更をコミット
    cur.close()
    conn.close()

def oll_check():
    if varckb0.get():
        varckb1.set(True)
        varckb2.set(True)
        varckb3.set(True)
    else:
        varckb1.set(False)
        varckb2.set(False)
        varckb3.set(False)

def log_screen():
    global varckb0,varckb1,varckb2,varckb3,var_1,var_2,var_3,ckb0,ckb1,ckb2,ckb3,rdo1,rdo2,rdo3,rdo4
    global varrgo, label_guidance,btn_log_show,btn_bk_top,scrollbar,textwidget,inp_name
    
    # top画面の選択ボタン削除
    button1.destroy()
    button2.destroy()
    button3.destroy()
    btn_log.destroy()  # 履歴ボタン削除

    # bool型変数定義
    var_1 = tk.BooleanVar()
    var_2 = tk.BooleanVar()
    var_3 = tk.BooleanVar()

    # 案内表示文　作成 配置　
    label_guidance = tk.Label(font=("HGP創英角ｺﾞｼｯｸUB", 15))
    label_guidance.place(x=200, y=5)
    text = "どのレベルのスコアを表示しますか"
    label_guidance["text"] = text

    # チェックボタン状態変数　作成
    varckb0 = tk.BooleanVar()
    varckb1 = tk.BooleanVar()
    varckb2 = tk.BooleanVar()
    varckb3 = tk.BooleanVar()
    
    varckb0.set(False)
    varckb1.set(False)
    varckb2.set(False)
    varckb3.set(False)
    
    # チェックボタン　作成
    ckb0 = tk.Checkbutton(text="全て", font=("HGP創英角ｺﾞｼｯｸUB", 15), variable=varckb0,command=oll_check)
    ckb1 = tk.Checkbutton(text="初級", font=("HGP創英角ｺﾞｼｯｸUB", 15), variable=varckb1)
    ckb2 = tk.Checkbutton(text="中級", font=("HGP創英角ｺﾞｼｯｸUB", 15), variable=varckb2)
    ckb3 = tk.Checkbutton(text="上級", font=("HGP創英角ｺﾞｼｯｸUB", 15), variable=varckb3)

    # チェックボタン　配置
    ckb0.place(x=100, y=40)
    ckb1.place(x=200, y=40)
    ckb2.place(x=300, y=40)
    ckb3.place(x=400, y=40)

    #名前検索　作成　配置
    inp_name = tk.Entry(root,font = ("Times New Roman" , 14),width=15)
    inp_name.place(x=500, y=45)
    
    # 表示ボタン　作成　配置
    btn_log_show = tk.Button(root, text="表示", font=("HGP創英角ｺﾞｼｯｸUB", 15), command=selectb_db)
    btn_log_show.place(x=650, y=40)

    # ラジオボタンにチェックを入れる
    varrgo = tk.IntVar()
    varrgo.set(1)  # 初期設定

    # ラジオボタン 作成
    rdo1 = tk.Radiobutton(root, text='新しい順', font=("Times New Roman", 10), value=1, variable=varrgo)
    rdo2 = tk.Radiobutton(root, text='古い順', font=("Times New Roman", 10), value=2, variable=varrgo)
    rdo3 = tk.Radiobutton(root, text='早い順', font=("Times New Roman", 10), value=3, variable=varrgo)
    rdo4 = tk.Radiobutton(root, text='遅い順', font=("Times New Roman", 10), value=4, variable=varrgo)

    # ラジオボタン 配置
    rdo1.place(x=650, y=100)
    rdo2.place(x=650, y=130)
    rdo3.place(x=650, y=160)
    rdo4.place(x=650, y=190)

    # top戻るボタン　　作成　配置
    btn_bk_top = tk.Button(root, text="トップに戻る", width=10, height=3, bg="#696969", fg="#ffffff", command=log_to_top_scrern)
    btn_bk_top.place(x=500, y=500)

    # テキストウィジェット　スクロールバー　作成
    scrollbar = tk.Scrollbar(root)
    textwidget = tk.Text(root,font=("Times New Roman", 11))
    textwidget.place(x=100, y=100, height=370, width=500)
    scrollbar.place(x=600, y=100,height = 350)  # スクロールバーをテキストウィジェットの隣に配置
    scrollbar.config(command=textwidget.yview)
    textwidget.config(yscrollcommand=scrollbar.set, state="disabled")

    # Tkinterのイベントループを開始する
    root.mainloop()

def count_down():
    global tmr
    
    label_cnt["text"] = tmr
    
    if tmr > 0 :
        tmr -= 1
        root.after(1000,count_down)
    elif  tmr == 0 :
        create_question()
    else:
        label_cnt.pack_forget()

def create_question():
    global r,st,fg
    btn_replay["state"] = "normal"
    btn_bk_top["state"] = "normal"
    
    fg = True

    #カウントラベル削除
    label_cnt.destroy()
    
    if level == 1:
        ALP = ["0","1","2","3","4","5","6","7","8","9","10"]
    elif level == 2:
        ALP = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    elif level ==3:
        ALP = ["愛知","秋田","青森","千葉","愛媛","福井","福岡","福島","岐阜","群馬","広島","北海道","兵庫","茨城","石川","岩手","香川","鹿児島","神奈川","高知","熊本","京都","三重","宮城","宮崎","長野","長崎","奈良","新潟","大分","岡山","沖縄","大阪","佐賀","埼玉","滋賀","島根","静岡","栃木","徳島","東京","鳥取","富山","和歌山","山形","山口","山梨"]
    
    #文字列シャフル
    random.shuffle(ALP)
    r = random.choice(ALP)
    print(r)
    
    ALP.remove(r)
    label_str["text"] = ALP
    
    #テキストの入力禁止を解除
    entry.configure(state='normal')
    
    #タイマースタート
    st = time.time()

def game_screen(num):
    global tmr,btn_bk_top,miss,btn_replay,level,entry,btn_ist_name
    global label_str,label_cnt,label_msg,label_miss,button1,button2,button3
    
    tmr = 3#初期値設定：タイマー（3）
    miss = 0#初期値設定：失敗数
    level = num#level設定
    
    # top画面の選択ボタン削除
    button1.destroy()
    button2.destroy()
    button3.destroy()
    
    btn_log.destroy()#履歴ボタン削除

    #label　作成
    label_cnt = tk.Label(font = ("HGP創英角ｺﾞｼｯｸUB" , 80))#時間
    label_str = tk.Label(font = ("HGP創英角ｺﾞｼｯｸUB" , 20),wraplength=700)#問題
    label_msg = tk.Label(font = ("HGP創英角ｺﾞｼｯｸUB" , 15))#解答
    label_miss = tk.Label(font = ("HGP創英角ｺﾞｼｯｸUB" , 15))#失敗回数
    
    #label　設置
    label_cnt.pack()
    label_str.pack(pady=40)
    label_msg.pack()
    label_miss.pack()
    
    #戻るボタン　作成　配置
    btn_bk_top = tk.Button(root,text="戻る",width=10,height=3,bg="#696969",fg="#ffffff",command = game_to_top_scrern,state = "disable")    
    btn_bk_top.place(x=500,y=500)
    
    #replayボタン　作成　配置
    btn_replay = tk.Button(root,text="リプレイ",width=10,height=3,bg="#696969",fg="#ffffff",command = lambda:replay(),state = "disable")    
    btn_replay.place(x=600,y=500)
    
    #テキストボックス設置
    entry = tk.Entry(root,font = ("Times New Roman" , 15),width=20,justify="center")
    entry.bind("<Return>", key_down)
    entry.place(x=300, y=400)
    entry.configure(state='readonly')#テキストの入力禁止
    
    btn_ist_name = tk.Button(root,text="名前を登録",command = register) 
    btn_ist_name.place_forget()
    
    count_down()

def replay():
    global btn_ist_name
    
    #削除
    label_cnt.destroy()
    label_str.destroy()
    label_msg.destroy()
    label_miss.destroy()
    entry.destroy()     #入力ボックス
    btn_bk_top.destroy()#topに戻るボタン
    btn_replay.destroy()#リプレイ
    
    btn_ist_name["state"] = "normal"
    btn_ist_name.destroy()
    
    #top画面
    game_screen(level)

def key_down(event):
    global miss,time_,btn_ist_name,fg
    
    #入力取得
    key = entry.get()
    print(key.upper())
    
    #入力欄削除
    entry.delete(0, tk.END) 
    
    if key.upper() == r and fg:
        fg = False
        et = time.time()
        n = 4 #少数切り捨て桁
        time_ = math.floor((et - st) * 10 ** n) / (10 ** n)
        times = "解答  '" + r + "'  Time :" + str(time_) + "s"
        label_msg["text"] = times
        
        #名前登録button
        btn_ist_name = tk.Button(root,text="名前を登録",command = register)    
        btn_ist_name.place(x=500,y=400)

    if fg:
        miss += 1
        temp = "失敗数：ｘ" + str(miss)
        label_miss["text"]  = temp

def game_to_top_scrern():  
    global btn_ist_name
    
    #label削除
    label_cnt.destroy()
    label_str.destroy()
    label_msg.destroy()
    label_miss.destroy()
    entry.destroy()#入力ボックス削除
    btn_bk_top.destroy()#topに戻るボタン削除
    btn_replay.destroy()#リプレイ削除
    btn_ist_name.destroy()
    #top画面
    main()

def log_to_top_scrern():
    #削除
    label_guidance.destroy()
    ckb0.destroy()
    ckb1.destroy()
    ckb2.destroy()
    ckb3.destroy()
    btn_log_show.destroy()
    rdo1.destroy()
    rdo2.destroy()
    rdo3.destroy()
    rdo4.destroy()
    btn_log_show.destroy()
    rdo1.destroy()
    rdo2.destroy()
    rdo3.destroy()
    inp_name.destroy()
    btn_bk_top.destroy()
    scrollbar.destroy()
    textwidget.destroy()
    
    #top画面
    main()

def main():
    global root,entry,button1,button2,button3,btn_log


    #level選択ボタン　作成
    button1 = tk.Button(root,text="初級",font=("HGP創英角ｺﾞｼｯｸUB" , 20),width=10,height=3,bg="#696969",fg="#ffffff",command = lambda:game_screen(1))
    button2 = tk.Button(root,text="中級",font=("HGP創英角ｺﾞｼｯｸUB" , 20),width=10,height=3,bg="#696969",fg="#ffffff",command = lambda:game_screen(2))
    button3 = tk.Button(root,text="上級",font=("HGP創英角ｺﾞｼｯｸUB" , 20),width=10,height=3,bg="#696969",fg="#ffffff",command = lambda:game_screen(3))
    #level選択ボタン　配置
    button1.place(x=100,y=200)
    button2.place(x=300,y=200)
    button3.place(x=500,y=200)
    
    #履歴ボタン　作成　配置
    btn_log = tk.Button(root,text="履歴",width=10,height=3,bg="#696969",fg="#ffffff",command = log_screen)    
    btn_log.place(x=500,y=500)

    # Tkinterのイベントループを開始する
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("文字あてゲーム")
    root.geometry("800x600")
    main()
