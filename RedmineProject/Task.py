class Task(object):
    Redmine_user_id = ''
    Canonicalname= ''
    Email = ''

    def __init__(self,Redmine_user_id,Canonicalname,Email):
        self.Redmine_user_id = Redmine_user_id
        self.Canonicalname = Canonicalname
        self.Email = Email

    def edit_task(self):
        print ('1 - Redmine_user_id \n'
               '2 - Canonical name \n'
               '3 - Email ')

        num_edit = str(input())
        if num_edit == '1':
            print("Enter value of field: ")
            value = str(input())
            self.Redmine_user_id = value
            return True
        elif num_edit == '2':
            print("Enter value of field: ")
            value = str(input())
            self.Canonicalname = value
            return True
        elif num_edit == '3':
            print("Enter value of field: ")
            value = str(input())
            self.Email = value
            return True
        else:
            print ("Field is not exist or can not be changed")
            return False












