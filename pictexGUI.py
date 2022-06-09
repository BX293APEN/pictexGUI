#!/usr/bin/env python
# -*- coding: utf8 -*-
import tkinter
import tkinter.messagebox as messagebox
import tkinter.filedialog
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
from PIL import Image
import pyocr
import os
import subprocess
import traceback

#操作定義
def closewindow():
    statusbar["text"] = "確認"
    msgvalue = messagebox.askquestion( "確認", "終了しますか？")
    if msgvalue == "yes":
        body.destroy()
    else:
        statusbar["text"] = "続行"
        
def right_click_menu(event):
    #右クリック設定
    name = str(event.widget.extra)
    right_menu = tkinter.Menu(eval(name), tearoff=0, font=("HGPｺﾞｼｯｸE", 15))
    right_menu.add_command(label="コピー",command = lambda:copytxt(name))
    right_menu.add_separator()
    right_menu.add_command(label="貼り付け",command = lambda:pastetxt(name))
    right_menu.post(event.x_root, event.y_root)
    
def copytxt(wname):
    try:
        eval(wname).clipboard_clear()
        if wname == "textarea":
            cptxt = eval(wname).get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        else:
            cptxt = eval(wname).selection_get()
        eval(wname).clipboard_append(cptxt)
        statusbar["text"] = cptxt  + " をコピー"
    except:
        statusbar["text"] = "コピー出来ませんでした"
        eval(wname).clipboard_clear()
    
def pastetxt(wname):
    try:
        pttxt = eval(wname).clipboard_get()
        eval(wname).insert(tkinter.INSERT, pttxt)
        statusbar["text"] = "貼り付け" + pttxt
    except:
        statusbar["text"] = "貼り付け出来ませんでした"

def cmd(event):
    command = cmdbox.get()
    r = subprocess.check_output(command, shell=True)
    cmdvalue = r.decode("ANSI").strip()
    statusbar["text"] = command + " を実行しました"
    textarea.delete("1.0","end")
    textarea.insert('1.0', cmdvalue)
    cmdbox.delete(0, tkinter.END)
    
def stchange_textbox1(event):
    statusbar["text"] = "テキスト変換する画像のパスを入力してください"

def stchange_textarea(event):
    statusbar["text"] = "テキストエリア"

def stchange_cmd(event):
    statusbar["text"] = "コマンドを入力してください"

def combobox_func(event):
    statusbar["text"] = combobox.get() + "で変換します"
    
def button_sansho_func():
    filetype = [("PNG画像","*.png"), ("JPEG形式画像","*.jpg;*.jpeg"), ("すべてのファイル","*")]
    file_path = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = dire)
    textbox1.delete(0, tkinter.END)
    textbox1.insert(tkinter.END,file_path)
    statusbar["text"] = file_path + "を変換"
    
def save():
    filetype = [("テキストファイル","*.txt"), ("すべてのファイル","*")]
    file_path = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = dire)
    statusbar["text"] = "確認"
    msgvalue = messagebox.askquestion( "確認", file_path + "\nにテキストを保存しますか？")
    if msgvalue == "yes":
        try:
            f = open(file_path, 'w+', encoding = "utf-8")
            savetext = textarea.get("1.0", "end-1c")
            f.write(savetext)
            f.close()
            statusbar["text"] = file_path + "に保存"
        except:
            statusbar["text"] = "保存出来ません"
    else:
        statusbar["text"] = "中止" #ステータスバーの更新
    
def button_run_func():
    text = textbox1.get()
    statusbar["text"] = "確認"
    msgvalue = messagebox.askquestion( "確認", text + "\nをテキストに変換しますか？")
    if msgvalue == "yes":
        statusbar["text"] = "実行" #ステータスバーの更新
        try:
            pictext = engine.image_to_string(Image.open(text), lang = combobox.get())
            textarea.delete("1.0","end")
            textarea.insert('1.0', pictext)
            messagebox.showinfo('確認', '実行しました')
            statusbar["text"] = "成功"
        except:
            textarea.delete("1.0","end")
            statusbar["text"] = "失敗"
            messagebox.showerror("ERROR", "読み取り失敗\n" + traceback.format_exc()) # エラー取得
    else:
        statusbar["text"] = "中止" #ステータスバーの更新
        textbox1.delete(0, tkinter.END)  # テキストボックスの中身を初期化する
        textbox1.insert(tkinter.END,dire)


#変数設定
dire = os.getcwd().replace(os.path.sep, '/')

#ウィンドウ設定
body = tkinter.Tk()
body.title(u"pictexGUI") # ウィンドウタイトル
body.geometry("800x500") # ウィンドウサイズ
body.configure(background = 'white')
body.resizable(0,0)
body.iconbitmap(dire + "/icon/vscode.ico")

#メニューボタン
menu_bar = tkinter.Menu(body)
body.config(menu = menu_bar)
menu_file = tkinter.Menu(menu_bar, tearoff=0, font=("HGPｺﾞｼｯｸE", "10"))
menu_file.add_command(label='開く', command=button_sansho_func)
menu_file.add_separator()
menu_file.add_command(label='保存', command=save)

menu_bar.add_cascade(label='ファイル', menu = menu_file) 
menu_bar.add_cascade(label='閉じる', command=closewindow)


#ボタン
button_run = tkinter.Button(body, text = "実行", command = button_run_func , font=("HGPｺﾞｼｯｸE", "15"))
button_run.pack(padx=20,pady = 45, anchor=tkinter.NE, expand=True, ipadx=30)

button_sansho = tkinter.Button(body, text = "参照", width = 10,command = button_sansho_func,  font=("HGPｺﾞｼｯｸE", "15"))
button_sansho.place(x=530 ,y = 45)

#テキストボックス
textbox1 = tkinter.Entry(body, width = 70 ,foreground='#0f00ff', font=("HGPｺﾞｼｯｸE", "15"),relief = tkinter.SOLID) 
textbox1.extra = "textbox1" # extraで変数名を登録
textbox1.place(x = 10, y = 10)
textbox1.insert(tkinter.END,dire)
textbox1.bind('<Button>', stchange_textbox1)#左クリックが押されたら
textbox1.bind("<Button-3>", right_click_menu)#右クリックが押されたら

textarea = scrolledtext.ScrolledText(body, font=("HGPｺﾞｼｯｸE", 15), height=15, width=65)
textarea.extra = "textarea" # extraで変数名を登録
textarea.place(x = 10, y = 90)
textarea.bind('<Button>', stchange_textarea)#左クリックが押されたら
textarea.bind("<Button-3>", right_click_menu)#右クリックが押されたら

cmdbox = tkinter.Entry(body, width = 72 ,background = "black",foreground='#00ff00', font=("HGPｺﾞｼｯｸE", "15"), bd=0, insertbackground="#00ff00", insertwidth = 5)
cmdbox.extra = "cmdbox" # extraで変数名を登録
cmdbox.place(x = 23, y = 420,height=30)
cmdbox.bind('<Return>', cmd) #Enterキーが押されたら
cmdbox.bind('<Button>', stchange_cmd)#左クリックが押されたら
cmdbox.bind("<Button-3>", right_click_menu)#右クリックが押されたら

#テキスト表示
langLabel = tkinter.Label(body, text='言語を選択:', font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
langLabel.place(x = 10, y = 50)
cmdLabel = tkinter.Label(body, text='$>', font=("HGPｺﾞｼｯｸE", "15"),background = "black",foreground='#00ff00',bd=0)
cmdLabel.place(x = 0, y = 420,height=30)

#セレクトボックス
engines = pyocr.get_available_tools()
engine = engines[0]
langs = engine.get_available_languages() # 対応言語取得
jpn = langs.index("jpn") # jpnの要素番号を取得
selectvalue = tkinter.StringVar()
combobox = ttk.Combobox(body,state="readonly" ,values=langs, justify="left", textvariable= selectvalue, font=("HGPｺﾞｼｯｸE", "15"),foreground='#000000')
combobox.place(x = 120, y = 50)
combobox.bind('<<ComboboxSelected>>', combobox_func)
combobox.current(jpn)


#ステータスバー
statusbar = tkinter.Label(body, text = "起動しました", bd = 1, relief = tkinter.SUNKEN, anchor = tkinter.W)
statusbar.pack(side = tkinter.BOTTOM, fill = tkinter.X)

body.mainloop() # ずっと表示させる