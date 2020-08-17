import mysql.connector


class DbConnector(object):
    """docstring for DbConnector"""

    def __init__(self, host, user, passwd, database):
        super(DbConnector, self).__init__()
        self.db = mysql.connector.connect(
            host=host, user=user, passwd=passwd, database=database)
        self.cursor = self.db.cursor()

    def add_user(self, user_id, first_name):
        self.cursor.execute(
            "INSERT INTO users (`id`, `name`) VALUES({},'{}')".format(user_id, first_name))

    def user_exists(self, user_id):
        self.cursor.execute(
            "SELECT * FROM `users` WHERE `id` = '{}'".format(user_id))
        result = self.cursor.fetchall()
        return bool(len(result))

    def list_tasks(self, user_id):
        self.cursor.execute(
            "SELECT * FROM `tasks` WHERE `user_id` = '{}'".format(user_id))
        return self.cursor.fetchall()

    def add_task(self, task_name, user_id):
        self.cursor.execute(
            "INSERT INTO tasks (name,user_id) VALUES ('{}',{})".format(task_name, user_id))

    def pop_task(self, count, user_id):
        self.cursor.execute(
            "SELECT * FROM `tasks` WHERE `user_id` = '{}'".format(user_id))
        tasks = self.cursor.fetchall()
        task_id = tasks[count - 1][0]
        self.cursor.execute(
            "DELETE FROM `todolist`.`tasks` WHERE (`task_id` = {});".format(task_id))
        return tasks[count - 1][1]
