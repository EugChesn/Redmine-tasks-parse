class User(object):

    def __init__(self,firstname,lastname,office,mail,redmine_id,login):
        self.firstname = firstname
        self.lastname = lastname
        self.office = office
        self.mail = mail
        self.redmine_id = redmine_id
        self.canonical_name = login


    def print_user(self):
        print ("Id  " + str(self.redmine_id))
        print ("Canonical name  " + self.canonical_name)

    def edit_task_user(self):

        print ('1 - Redmine_user_id \n'
               '2 - Canonical name \n'
               '3 - Email \n'
               '4 - Office')

        num_edit = str(input())
        value = str(raw_input('Enter value of field:  '))
        if num_edit == '1':
            self.redmine_id = value
            return True
        elif num_edit == '2':
            self.canonical_name = value
            return True
        elif num_edit == '3':
            self.mail = value
            return True
        elif num_edit == '4':
            self.office = value
            return True
        else:
            print ("Field is not exist or can not be changed")
            return False

    def get_user_string(self):
        return self.firstname + ' '  + self.lastname

    def equal(self,user):
        if self.canonical_name == user.canonical_name and self.office == user.office:
            return True
        else:
            return False

if __name__ == '__main__':
    print('Please run to RedmineScript.py')