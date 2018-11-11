# -*- coding: utf-8 -*-

import sqlite3

global_db_path = '/Users/liuye/.mpwddb/mpwd3.db'


class Sqlite3Factory:

    def __init__(self, db_connection):
        """
        获取密码数据库的链接
        :param db_connection: 数据库链接
        """
        self.db_connection = db_connection

    def obtain_db_conn(self):
        """
        获取数据链接
        :return:
        """
        db_conn = self.db_connection
        try:
            if not db_conn:
                db_conn = sqlite3.connect(global_db_path)
                self.db_connection = db_conn
        except Exception as err:
            print('get db connection error --==>>' + err)
        return db_conn

    def close_db(self):
        """
        关闭数据库
        :return:
        """
        db_conn = self.db_connection
        if db_conn:
            db_conn.close()

    def init_db(self):
        """
        初始化数据库
        :return:
        """
        db_conn = self.obtain_db_conn()
        cursor = db_conn.cursor()
        # 创建密码存储表
        init_sql = """
            CREATE TABLE pwd_store (
              id        INTEGER PRIMARY KEY AUTOINCREMENT,
              label     VARCHAR NOT NULL UNIQUE,
              login     VARCHAR NOT NULL,
              password  VARCHAR NOT NULL,
              ismore    VARCHAR NOT NULL,
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

    def drop_db(self):
        """
        删除数据
        :return:
        """
        db_conn = self.obtain_db_conn()
        drop_sql = """DROP TABLE IF EXISTS pwd_store;"""
        print('execute drop sql:[{}]'.format(drop_sql))
        cursor = db_conn.cursor()
        cursor.execute(drop_sql)
        db_conn.commit()
        print('table is droped!')

    def append_pwd(self):
        """
        添加密码记录
        :return:
        """
        db_conn = self.obtain_db_conn()
        label = input('input label: ').strip()
        if label == '':
            return False

        login = input('input login: ').strip()
        password = input('input password: ').strip()
        question1 = False
        answer1 = False
        question2 = False
        answer2 = False
        question3 = False
        answer3 = False
        memo = False

        ismore = input('more pwd info?[Y/n]').strip()

        if ismore == 'Y':
            question1 = input('input question1: ').strip()
            answer1 = input('input answer1: ').strip()
            question2 = input('input question2: ').strip()
            answer2 = input('input answer2: ').strip()
            question3 = input('input question3: ').strip()
            answer3 = input('input answer3: ').strip()
            memo = input('input memo: ').strip()
        else:
            pass

        cursor = db_conn.cursor()

        insert_sql = """
        insert into
        pwd_store
        (label, login, password, ismore, question1, answer1, question2, answer2, question3, answer3, memo)
        values
        (:label, :login, :password, :ismore, :question1,:answer1, :question2, :answer2, :question3, :answer3, :memo);
        """

        insert_data = {'label': label, 'login': login, 'password': password, 'ismore': ismore,
                       'question1': question1, 'answer1': answer1, 'question2': question2, 'answer2': answer2,
                       'question3': question3, 'answer3': answer3, 'memo': memo}
        cursor.execute(insert_sql, insert_data)
        db_conn.commit()

        return True

    def lookup_pwd(self):
        """
        查询密码
        :return:
        """
        label = input('input label: ').strip()
        if label == '':
            return False

        db_conn = self.obtain_db_conn()
        cursor = db_conn.cursor()
        lookup_sql = """
        select id,
          label,
          login,
          password,
          ismore,
          question1,
          answer1,
          question2,
          answer2,
          question3,
          answer3,
          memo 
        from pwd_store 
        where 1=1 and label like (:label) order by id desc;"""
        lookup_data = {'label': label}
        cursor.execute(lookup_sql, lookup_data)
        result = cursor.fetchall()
        if len(result) == 0:
            print('\033[1;31;mno matching record!\033[0m')
            return True
        single_rec = result[0]
        login = single_rec[2]
        password = single_rec[3]
        ismore = single_rec[4]
        question1 = single_rec[5]
        answer1 = single_rec[6]
        question2 = single_rec[7]
        answer2 = single_rec[8]
        question3 = single_rec[9]
        answer3 = single_rec[10]
        memo = single_rec[11]

        print('\033[1;34;m' + str(login) + ' = ' + str(password) + ' = ' + str(memo) + '\033[0m')
        if ismore == 'Y':
            print('\033[1;34;m' + str(question1) + ' = ' + str(answer1) + '\033[0m')
            print('\033[1;34;m' + str(question2) + ' = ' + str(answer2) + '\033[0m')
            print('\033[1;34;m' + str(question3) + ' = ' + str(answer3) + '\033[0m')
        return True

    def list_all_label(self):
        """
        列出所有标题
        :return:
        """
        db_conn = self.obtain_db_conn()
        cursor = db_conn.cursor()
        label_sql = """
        select label from pwd_store where 1=1 order by id desc;"""
        cursor.execute(label_sql)
        results = cursor.fetchall()
        label_list = []
        for rec in results:
            label_list.append(rec[0])

        print(label_list)

    def list_all_pwd(self):
        """
        列出所有密码
        :return:
        """
        db_conn = self.obtain_db_conn()
        cursor = db_conn.cursor()
        lookup_sql = """
        select id,
          label,
          login,
          password,
          ismore,
          question1,
          answer1,
          question2,
          answer2,
          question3,
          answer3,
          memo 
        from pwd_store 
        where 1=1 order by id desc;"""
        cursor.execute(lookup_sql)
        results = cursor.fetchall()
        print('\033[1;31;m--------------------this is begin of result!--------------------\033[0m')
        for rec in results:
            id = rec[0]
            label = rec[1]
            login = rec[2]
            password = rec[3]
            ismore = rec[4]
            question1 = rec[5]
            answer1 = rec[6]
            question2 = rec[7]
            answer2 = rec[8]
            question3 = rec[9]
            answer3 = rec[10]
            memo = rec[11]
            print('\033[1;34;m' + str(id) + ' = ' + str(label) + '\033[0m')
            print('\033[1;34;m' + str(login) + ' = ' + str(password) + ' = ' + str(memo) + '\033[0m')
            if ismore == 'Y':
                print('\033[1;34;m' + str(question1) + ' = ' + str(answer1) + '\033[0m')
                print('\033[1;34;m' + str(question2) + ' = ' + str(answer2) + '\033[0m')
                print('\033[1;34;m' + str(question3) + ' = ' + str(answer3) + '\033[0m')
            print('\033[1;31;m---------------------------------------------------------\033[0m')
        print('\033[1;31;m---------------------this is end of result!---------------------\033[0m')

    def update_pwd(self):
        """
        更新密码记录
        :return:
        """
        label = input('input delete label: ').strip()

        if label == '':
            return False

        lookup_sql = """
        select 
          id,
          label,
          login,
          password,
          ismore,
          question1,
          answer1,
          question2,
          answer2,
          question3,
          answer3,
          memo 
        from pwd_store 
        where 1=1 and label = (:label) 
        order by id desc;"""
        lookup_data = {'label': label}

        db_conn = self.obtain_db_conn()
        cursor = db_conn.cursor()
        cursor.execute(lookup_sql, lookup_data)
        pwd_records = cursor.fetchall()
        if len(pwd_records) == 0:
            print('\033[1;31;mno matching record!\033[0m')

        pwd_rec = pwd_records[0]

        question1 = pwd_rec[5]
        answer1 = pwd_rec[6]
        question2 = pwd_rec[7]
        answer2 = pwd_rec[8]
        question3 = pwd_rec[9]
        answer3 = pwd_rec[10]
        memo = pwd_rec[11]

        login = input('input login(\033[1;31;m' + pwd_rec[2] + '\033[0m): ').strip()
        if len(login) == 0:
            login = pwd_rec[2]

        password = input('input password(\033[1;31;m' + pwd_rec[3] + '\033[0m): ').strip()
        if len(password) == 0:
            password = pwd_rec[3]

        ismore = input('more pwd info(\033[1;31;m' + pwd_rec[4] + '\033[0m)?[Y/n]').strip()

        if ismore == 'Y':
            question1 = input('input question1(\033[1;31;m' + pwd_rec[5] + '\033[0m): ').strip()
            if len(question1) == 0:
                question1 = pwd_rec[5]
            answer1 = input('input answer1(\033[1;31;m' + pwd_rec[6] + '\033[0m): ').strip()
            if len(answer1) == 0:
                answer1 = pwd_rec[6]

            question2 = input('input question2(\033[1;31;m' + pwd_rec[7] + '\033[0m): ').strip()
            if len(question2) == 0:
                question2 = pwd_rec[7]
            answer2 = input('input answer2(\033[1;31;m' + pwd_rec[8] + '\033[0m): ').strip()
            if len(answer2) == 0:
                answer2 = pwd_rec[8]

            question3 = input('input question3(\033[1;31;m' + pwd_rec[9] + '\033[0m): ').strip()
            if len(question3) == 0:
                question3 = pwd_rec[9]
            answer3 = input('input answer3(\033[1;31;m' + pwd_rec[10] + '\033[0m): ').strip()
            if len(answer3) == 0:
                answer3 = pwd_rec[10]

            memo = input('input memo(\033[1;31;m' + pwd_rec[11] + '\033[0m): ').strip()
            if len(memo) == 0:
                memo = pwd_rec[11]
        else:
            ismore == 'Y'

        update_sql = """
        update pwd_store
            set login   = (:login), password = (:password), ismore = (:ismore), 
              question1 = (:question1), answer1   = (:answer1), question2 = (:question2), answer2 = (:answer2),
              question3 = (:question3), answer3 = (:answer3), memo = (:memo)
            where label = (:label);"""

        update_data = {'login': login, 'password': password, 'ismore': ismore,
                       'question1': question1, 'answer1': answer1, 'question2': question2, 'answer2': answer2,
                       'question3': question3, 'answer3': answer3, 'memo': memo, 'label': label}

        cursor.execute(update_sql, update_data)
        db_conn.commit()
        return True

    def delete_pwd(self):
        """
        删除密码
        :return:
        """
        db_conn = self.obtain_db_conn()
        label = input('input delete label: ').strip()
        if label == '':
            return False
        cursor = db_conn.cursor()
        delete_sql = """delete from pwd_store where label= (:label);"""
        delete_data = {'label': label}
        cursor.execute(delete_sql, delete_data)
        cursor.close()
        db_conn.commit()
        return True


def do_it():
    db_conn = False
    factory = Sqlite3Factory(db_conn)
    while True:
        choice = input('pwd>>>').strip()
        if choice == '':
            pass

        elif choice == 'reset' or choice == 'r':
            factory.drop_db()

        elif choice == 'init' or choice == 'i':
            factory.init_db()

        elif choice == 'exit' or choice == 'e':
            factory.close_db()
            print('bye bye!')
            break

        elif choice == 'help' or choice == 'h':
            try:
                factory.list_all_pwd()
            except Exception as err:
                print('lookup occur error:' + str(err))

        elif choice == 'append' or choice == 'a':  # todo append
            try:
                while True:
                    is_conn = factory.append_pwd()
                    if not is_conn:
                        break
                    print('append success!')
            except Exception as err:
                print('append occur error:' + str(err))

        elif choice == 'delete' or choice == 'd':  # todo delete
            try:
                while True:
                    is_conn = factory.delete_pwd()
                    if not is_conn:
                        break
                    print('delete success!')
            except Exception as err:
                print('delete occur error:' + str(err))

        elif choice == 'update' or choice == 'u':  # todo update
            try:
                while True:
                    is_conn = factory.update_pwd()
                    if not is_conn:
                        break
            except Exception as err:
                print('update occur error:' + str(err))

        elif choice == 'lookup' or choice == 'l':  # todo lookup
            try:
                while True:
                    is_conn = factory.lookup_pwd()
                    if not is_conn:
                        break
            except Exception as err:
                print('lookup occur error:' + str(err))

        elif choice == 'listall' or choice == 'la':  # todo list all
            try:
                factory.list_all_pwd()
            except Exception as err:
                print('lookup occur error:' + str(err))

        elif choice == 'listlabel' or choice == 'll':  # todo list title
            try:
                factory.list_all_label()
            except Exception as err:
                print('lookup occur error:' + str(err))

        else:
            pass


if __name__ == '__main__':
    do_it()
