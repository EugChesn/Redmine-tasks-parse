class User(object):
    firstname = ''
    lastname = ''

    def __init__(self,firstname,lastname):
        self.firstname = firstname
        self.lastname = lastname

    def get_user_string(self):
        return self.firstname + ' '  + self.lastname

    def equal(self,user):
        if self.firstname == user.firsname and self.lastname == self.lastname:
            return True
        else:
            return False