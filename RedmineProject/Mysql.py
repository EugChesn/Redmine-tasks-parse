import MySQLdb
import config
class MysqL(object):

    def __init__(self):
        try:
            self.db = MySQLdb.connect(host=config.HOST, user=config.USER, passwd=config.PASSWORD, db=config.DATABASE_NAME)
        except:
            self.db = None
            print 'Error connect'

    def mysqlConfirm(self,task_usr,issue,scop):
        if self.db is not None:
            try:
                redminetask = int(task_usr.redmine_id)
                username = task_usr.canonical_name
                email = task_usr.mail
                status = int(issue.status)
                scope =  scop #vpn

                cursor = self.db.cursor()
                cursor.execute("""INSERT INTO tasks(redminetask,redmineuser,username,email,scope,status) VALUES (%s,%s,%s,%s,%s,%s)""",(issue.id,redminetask,username,email,scope,status))
                self.db.commit()
                print('The data was successfully loaded')
            except:
                print 'Execute Error mysql'
                self.db.rollback()

    def mysqlSelect(self):
        if self.db is not None:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT * FROM tasks")
                row = cursor.fetchone()
                while row is not None:
                    print(row)
                    #r = row[0]
                    row = cursor.fetchone()
            except:
                print ("The data was successfully read")
                self.db.rollback()

    def mysqlClear(self):
        if self.db is not None:
            try:
                cursor = self.db.cursor()
                cursor.execute("DELETE FROM tasks")
                self.db.commit()
                print ('The database has been successfully cleaned')
            except:
                print ('Cleaning databases error!')
                self.db.rollback()

    def mysqlDelete(self,task_id):
        if self.db is not None:
            try:
                sql_str = "DELETE FROM tasks WHERE redminetask = '%s' "
                cursor = self.db.cursor()
                cursor.execute(sql_str, (task_id,))
                self.db.commit()
                print ('The database has been successfully cleaned')
            except:
                print ('Delete databases error!')
                self.db.rollback()

    def mysqlDisconnect(self):
        try:
            self.db.close()
            print ('Disconnect complete successful')
        except:
            print ('Disconnect db error')

if __name__ == '__main__':
    print('Please run to RedmineScript.py')


