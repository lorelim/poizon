import sqlite3


class SQLighter():

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()


    def add_user(self, chat_id, pr_message):
        with self.connection:
            self.cursor.execute("INSERT INTO `users` (`id`, `pr_message`) VALUES (?, ?)", (chat_id, pr_message))

    def check_user(self, chat_id):

        with self.connection:

            user = self.cursor.execute("SELECT * FROM `users` WHERE `id` = ?", (chat_id, )).fetchall()
        
        if len(user) > 0:
            return True
        else:
            return False

    def change_msg(self, chat_id, message_id):
        with self.connection:

            return self.cursor.execute("UPDATE `users` SET `pr_message` = ? WHERE `id` = ?", (message_id, chat_id ))

    def change_admin(self, chat_id, state):
        with self.connection:
            return self.connection.execute("UPDATE `users` SET `admin` = ? WHERE `id` = ?", (state, chat_id))

    def get_pr_msg(self, chat_id):

        with self.connection:

            return self.cursor.execute("SELECT `pr_message` FROM `users` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]


    def check_admin(self, chat_id):
        with self.connection:
            return self.cursor.execute("SELECT `admin` FROM `users` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]

    def get_cur(self, cur):

        if cur == "CNY":
            with self.connection:
                return self.cursor.execute("SELECT `CNY` FROM `currency`").fetchall()[0][0]

        if cur == "RUB":
            with self.connection:
                return self.cursor.execute("SELECT `RUB` FROM `currency`").fetchall()[0][0]

        if cur == "BYN":
            with self.connection:
                return self.cursor.execute("SELECT `BYN` FROM `currency`").fetchall()[0][0]

    def change_cur(self, cur, price):

        if cur == "CNY":
            with self.connection:
                return self.cursor.execute("UPDATE `currency` SET `CNY`= ?", (price, ))

        if cur == "RUB":
            with self.connection:
                return self.cursor.execute("UPDATE `currency` SET `RUB`= ?", (price, ))

        if cur == "BYN":
            with self.connection:
                return self.cursor.execute("UPDATE `currency` SET `BYN`= ?", (price, ))

    def get_cl_type(self, chat_id):
        with self.connection:
            return self.connection.execute("SELECT `cl_type` FROM `users` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]

    def change_cl_type(self, chat_id, cl_type):
        with self.connection:
            return self.connection.execute("UPDATE `users` SET `cl_type` = ? WHERE `id` = ?",(cl_type, chat_id))

    def get_state(self, chat_id):
        with self.connection:
            return self.connection.execute("SELECT `state` FROM `users` WHERE `id` = ?", (chat_id, )).fetchall()[0][0]

    def change_state(self, chat_id, state):
        with self.connection:
            return self.connection.execute("UPDATE `users` SET `state` = ? WHERE `id` = ?", (state, chat_id))
