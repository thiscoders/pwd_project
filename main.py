# -*- coding: utf-8 -*-

import os
import sqlite3

global_db_path = '/Users/liuye/.mpwddb/mpwd3.db'


def get_db_connect():
    connect = False
    try:
        connect = sqlite3.connect(global_db_path)
    except Exception as err:
        print("get db connection error --==>>" + err)
    return connect


def reset_db(db_conn=False):
    os.remove(global_db_path)
    init_db(db_conn)


def init_db(db_conn=False):
    cursor = db_conn.cursor()
    # 创建密码存储表
    init_sql = """
        CREATE TABLE pwd_store (
          id        INTEGER PRIMARY KEY AUTOINCREMENT,
          label     VARCHAR NOT NULL UNIQUE,
          username  VARCHAR NOT NULL,
          pwssword  VARCHAR NOT NULL,
          question1 VARCHAR,
          answer1   VARCHAR,
          question2 VARCHAR,
          answer2   VARCHAR,
          question3 VARCHAR,
          answer3   VARCHAR,
          memo      VARCHAR
        );"""
    cursor.execute(init_sql)
    index_sql = """CREATE INDEX index_label ON pwd_store (label);"""
    cursor.execute(index_sql)
    db_conn.commit()
    cursor.close()


def append_pwd(db_conn=False):
    label = input('input label: ').strip()
    username = input('input username: ').strip()
    pwssword = input('input pwssword: ').strip()
    question1 = False
    answer1 = False
    question2 = False
    answer2 = False
    question3 = False
    answer3 = False
    memo = False

    is_continue = input('is continue?(Y/n)').strip()

    if is_continue == 'Y':
        question1 = input('input question1: ').strip()
        answer1 = input('input answer1: ').strip()
        question2 = input('input question2: ').strip()
        answer2 = input('input answer2: ').strip()
        question3 = input('input question3: ').strip()
        answer3 = input('input answer3: ').strip()
    else:
        pass

    cursor = db_conn.cursor()
    insert_sql = """
    insert into pwd_store (label, username, pwssword, question1, answer1, question2, answer2, question3, answer3, memo)
    values (:label, :username, :pwssword, :question1, :answer1, :question2, :answer2, :question3, :answer3, :memo);
    """

    insert_data = {"label": label, "username": username,
                   "pwssword": pwssword, "question1": question1, "answer1": answer1, "question2": question2,
                   "answer2": answer2, "question3": question3, "answer3": answer3, "memo": memo}
    cursor.execute(insert_sql, insert_data)
    db_conn.commit()
    db_conn.close()


def update_pwd():
    pass


def delete_pwd():
    pass


def lookup_pwd():
    pass


def do_it(db_conn):
    while True:
        choice = input('pwd>>>').strip()
        if choice == '':
            pass
        elif choice == 'reset' or choice == '-2':
            reset_db(db_conn)
            break
        elif choice == 'init' or choice == '-1':
            init_db(db_conn)
        elif choice == 'exit' or choice == '0':
            print('bye bye!')
            break
        elif choice == 'append' or choice == '1':
            try:
                append_pwd(db_conn)
            except Exception as err:
                print('this is error:' + str(err))
        else:
            pass


if __name__ == '__main__':
    db_conn = False
    try:
        db_conn = get_db_connect()
        do_it(db_conn)
    except Exception as err:
        print('this is error:' + str(err))
        if db_conn:
            db_conn.rollback()
    finally:
        if db_conn:
            db_conn.close()
