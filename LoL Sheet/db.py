import requests
import wget
import os
import sqlite3

splash = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_0.jpg'
champ = 'http://ddragon.leagueoflegends.com/cdn/10.3.1/data/en_US/champion/{}.json'

churl = 'http://ddragon.leagueoflegends.com/cdn/10.4.1/data/en_US/champion.json'
req = requests.get(churl)
champs = req.json()
champions = [champ for champ in champs['data']]

def getNameOrderFromName(name):
    return champions.index(name) +1

def get_id(name):
    url = champ.format(name)
    req = requests.get(url)
    return req.json()['data'][name]['key']
class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS pool (id INTEGER PRIMARY KEY, chname, chid, chord)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM pool")
        rows = self.cur.fetchall()
        return rows

    def insert(self, champ):
        self.cur.execute("INSERT INTO pool VALUES (NULL, ?, ?, ?)",
                         (champ, get_id(champ), getNameOrderFromName(champ)))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM pool WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

