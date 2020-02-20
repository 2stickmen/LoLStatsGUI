import requests
import time
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import wget
from db import Database


db = Database('store.db')

apiKey = 'RGAPI-49b70ff5-5090-4132-a108-f7da98a20b65'
user = 'RestInKill'

def getIdFromName(username):
    url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'
    url = url.format(username,apiKey)
    response = requests.get(url)
    uid = response.json()['accountId']
    sid = response.json()['id']
    return uid, sid

ids = getIdFromName(user)
uid = ids[0]
sid = ids[1]
def champNameToNumber(champname):
    url = 'http://ddragon.leagueoflegends.com/cdn/10.1.1/data/en_US/champion.json'
    response = requests.get(url)
    return response.json()['data'][champname]['key']

def getMatchHistoryOnChamp(champname):
    cid = champNameToNumber(champname)
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?champion={}&api_key={}'
    url = url.format(uid,cid,apiKey)
    response = requests.get(url)
    return response.json()

def getGames(champ):
    history = getMatchHistoryOnChamp(champ)['matches']
    matches = []
    for i in history:
        gameId = i['gameId'] 
        url = 'https://euw1.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'
        url = url.format(gameId,apiKey)
        response = requests.get(url)
        matches.append(response.json())
    return matches
    

def getMastery(champname):
    cid = champNameToNumber(champname)
    url = 'https://euw1.api.riotgames.com//lol/champion-mastery/v4/champion-masteries/by-summoner/{}/by-champion/{}?api_key={}'
    url = url.format(sid,cid,apiKey)
    response = requests.get(url)
    return response.json()
    
def getLoadScreen(name):
    spurl = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_0.jpg'.format(name)
    wget.download(spurl)
    

def populate_list():
    champ_pool.delete(0, END)
    for row in db.fetch():
        champ_pool.insert(END, row)


def add_item():
    if champ_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(champ_text.get())
    getLoadScreen(champ_text.get())
    champ_pool.delete(0, END)
    champ_pool.insert(END, (champ_text.get()))
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = champ_pool.curselection()[0]
        selected_item = champ_pool.get(index)        
        chname = selected_item[1]
        champ_skin = ImageTk.PhotoImage(Image.open(skname.format(chname)))
        champ_panel.config(image = champ_skin)
        champ_panel.image = champ_skin
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    populate_list()






app = Tk()
# Code to add widgets will go here...
app.grid()


#Loadscreen Skin
skname = '{}_0.jpg'
champ_skin = ImageTk.PhotoImage(Image.open('Aatrox_0.jpg'))
champ_panel = Label(app, image = champ_skin)
champ_panel.image = champ_skin
champ_panel.grid(row=0,column=2,sticky=E,rowspan = 10, columnspan = 5, padx=5)
#addbox
champ_text = StringVar()
champ_label = Button(app, text = 'Add To Champ Pool',command=add_item)
champ_label.grid(row=1,column=0,sticky=N)
champ_entry = Entry(app, textvariable = champ_text)
champ_entry.grid(row=0,column=0)
#removebox
rem_label = Button(app, text = 'Remove Selected from Pool', command = remove_item)
rem_label.grid(row=3,column=0)
#Champ pool
champ_pool = Listbox(app,height = 30,width=30)
champ_pool.grid(row = 2, column = 0,sticky=W)
champ_pool.bind('<<ListboxSelect>>', select_item)
populate_list()
#Info Panel
info = Frame(app,height = 50,width=500)
info.grid(row=0,column=1)
infoTest = Label(info,text = 'Test :)')
infoTest.grid(row=0,column=0)
app.mainloop()



