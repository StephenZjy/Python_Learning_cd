import pymysql


class SqlOperation():
    def __init__(self):
        super(SqlOperation, self).__init__()
        self._init_connect()

    def _init_connect(self):
        self.conn = pymysql.connect(host='192.168.8.175', port=3306,
                                    user='user', passwd='Aa123456!',
                                    charset='utf8', db='userdb')
        self.cursor = self.conn.cursor()

    def insert_info(self, username, password, tel, email):
            sql = ('INSERT INTO user_info (username, password, tel, email) '
                   'VALUES (%(username)s, %(password)s, %(tel)s, %(email)s)')
            data = {
                'username': username,
                'password': password,
                'tel': tel,
                'email': email
            }
            self.cursor.execute(sql, data)
            self.conn.commit()

    def select_username(self, username):
        sql = "SELECT * FROM user_info WHERE username = %s"
        self.cursor.execute(sql, (username,))
        result = self.cursor.fetchone()

        return result



