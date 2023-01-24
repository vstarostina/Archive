import math
import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, login, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE login LIKE '{login}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким логином уже существует")
                return False
            ct = 1
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", (login, hpsw, ct))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД" + str(e))
            return False
        return True


    def addPost(self, text, sum):
        try:
            self.__cur.execute("INSERT INTO credit VALUES (NULL, ?, ?)", (text, sum))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления в БД" + str(e))
            return False
        return True


    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка при обращении к БД" + str(e))
        return False


    def getUserByLogin(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            print(login)
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res

        except sqlite3.Error as e:
            print("Ошибка добавления в БД" + str(e))

        return False







