#!/usr/bin/python
# -*- coding: utf-8 -*-

# File with the CRUD functions to interact
# with the database
#
# TODO: Proper rigorous cross-table indexing and integrity

import sqlite3
import sys
import os

def setup_db():
    con = sqlite3.connect('vocably.db')

    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='Users';")
        rows = cur.fetchall()
        if rows:
            cur.execute("DROP TABLE Users;")

        cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='Vocab';")
        rows = cur.fetchall()
        if rows:
            cur.execute("DROP TABLE Vocab;")

        cur.execute("CREATE TABLE Users(Email TEXT, Score REAL, CONSTRAINT unq UNIQUE (Email, Score), PRIMARY KEY (Email));")

        cur.execute("CREATE TABLE Vocab(Email TEXT, word TEXT, CONSTRAINT unq UNIQUE (Email, word));")

        print "Success: Database set up"

def create_user(email, score):
    con = sqlite3.connect('vocably.db')

    with con:
        query = 'INSERT INTO Users (Email,Score) VALUES("'
        query += email + '",' + str(score) + ');'
        cur = con.cursor()
        try:
            cur.execute(query)
        except sqlite3.IntegrityError:
            print "Problem creating user " + email

def set_score(email, score):
    con = sqlite3.connect('vocably.db')

    with con:
        query = 'UPDATE Users SET Score = '
        query += str(score) + ' WHERE Email = "'
        query += email + '";'
        cur = con.cursor()
        cur.execute(query)

def get_list(email):
    con = sqlite3.connect('vocably.db')

    with con:
        cur = con.cursor()
        query = 'SELECT word FROM Vocab WHERE Email="'+email+'";'
        cur.execute(query)
        rows = cur.fetchall()
        return [row[0] for row in rows]

def get_score(email):
    con = sqlite3.connect('vocably.db')

    with con:
        cur = con.cursor()
        query = 'SELECT score FROM Users WHERE email="'+email+'";'
        cur.execute(query)
        rows = cur.fetchall()
        return rows[0][0] if rows else None

def store_user_words(email,words):
    con = sqlite3.connect('vocably.db')

    with con:
        cur = con.cursor()

        for word in words:
            query = 'INSERT INTO Vocab VALUES("'
            query += email + '","' + word + '");'
            try:
                cur.execute(query)
            except sqlite3.IntegrityError:
                pass

def wipe_db():

    if not os.path.isfile("vocably.db"):
        print "The database is not there to begin with!"
        return

    msg = "Are you 100% sure you want to wipe the database?\n"
    msg += "This will remote all data and is irreversible... (yes/no)\n"
    input_ = raw_input(msg).strip().lower()

    if input_=="yes":
        os.remove("vocably.db")
        print "Database wiped"
    else:
        print "OK, database wipe out aborted"

def test():
    # Test the above suite of functions
    wipe_db()
    setup_db()
    create_user("test@user.com",0.2323)
    create_user("test2@user.com",0.3427)
    create_user("test@user.com",0.3726)
    set_score("test2@user.com",0.9999)
    store_user_words("test@user.com",['helicopter','giraffe','heteroskedasticity'])
    store_user_words("test@user.com",['computer','giraffe','fantastic'])
    print get_list('test@user.com')
    print get_score('test2@user.com')
    print get_score('test3@user.com')

if __name__ == "__main__":
    test()
