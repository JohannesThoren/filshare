# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import sqlite3

con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()


def execute_query(query: str):
    cur.execute(query)
    con.commit()


def create_table():
    t = """CREATE TABLE IF NOT EXISTS files (uid TEXT, filename TEXT, pass TEXT, email TEXT)"""
    execute_query(t)

def get_file_information(uid):
    q = f"SELECT * FROM files WHERE (uid = '{uid}')"
    cur.execute(q)
    d = cur.fetchone()
    con.commit()

    return d


def add_file(uid, filename, email, file_password):
    q = "INSERT INTO files VALUES (?, ?, ?, ?)"

    print(q)
    cur.execute(q, (uid, filename, file_password, email))
    con.commit()