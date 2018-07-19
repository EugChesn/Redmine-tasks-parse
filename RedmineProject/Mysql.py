import MySQLdb
import config
class MysqL(object):

    def __init__(self):
        try:
            self.db = MySQLdb.connect(host=config.HOST, user=config.USER, passwd=config.PASSWORD, db=config.DATABASE_NAME)
        except:
            self.db = None
            print 'Error connect'

    def mysqlConfirm(self,task,numt):
        if self.db is not None:
            try:
                redminetask = int(task.Redmine_user_id)
                username = task.Canonicalname
                email = task.Email
                num = numt
                scope = 1 #vpn
                status = 1 #new

                cursor = self.db.cursor()
                cursor.execute("""INSERT INTO tasks(redminetask,redmineuser,username,email,scope,status) VALUES (%s,%s,%s,%s,%s,%s)""",(num,redminetask,username,email,scope,status))
                self.db.commit()
                print('The data was successfully loaded')
            except:
                print 'Execute Error mysql'
                self.db.rollback()



