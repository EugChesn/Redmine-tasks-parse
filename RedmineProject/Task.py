class Task(object):
    Redmine_user_id = ''
    Canonicalname= ''
    Firstname = ''
    Lastname = ''
    Email = ''

    Scope = ''
    Assigned_to = ''
    Status = ''
    Subject = ''
    Description = ''
    Name_project = ''


    def __init__(self,Scope,Redmine_user_id,Canonicalname,
                 Firstname,Lastname,Assigned_to,Email,
                 Status,Subject,Description,Name_project):

        self.Scope = Scope
        self.Redmine_user_id = Redmine_user_id
        self.Canonicalname = Canonicalname
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Assigned_to = Assigned_to
        self.Email = Email
        self.Status = Status
        self.Subject = Subject
        self.Description = Description
        self.Name_project = Name_project

    def print_task(self):
        print('Scope:  ' + self.Scope)
        print("Redmine user id:  " + self.Redmine_user_id)
        print('Canonical name:  ' + self.Canonicalname)
        print('Firstname:  ' + self.Firstname)
        print('Lastname:  ' + self.Lastname)
        print ("Assigned to:  " + self.Assigned_to)
        print("Email:  " + self.Email)
        print ("Status:  " + self.Status)
        print ("Subject:  " + self.Subject)
        print ("Description:  " + self.Description)
        print ("Name of project:  " + self.Name_project)

    def edit_task(self,field,value):
        if field == 'Scope':
            self.Scope = value
        elif field == 'Redmine_user_id':
            self.Redmine_user_id =value
        elif field == 'Canonicalname':
            self.Canonicalname = value
        elif field == 'Firstname':
            self.Firstname = value
        elif field == 'Lastname':
            self.Lastname = value
        elif field == 'Assigned_to':
            self.Assigned_to = value
        elif field == 'Email':
            self.Email = value
        elif field == 'Status':
            self.Status = value
        elif field == 'Subject':
            self.Subject =value
        elif field == 'Description':
            self.Description = value
        elif field == 'Name_project':
            self.Name_project = value
        else:
            print ("Field is not exist")












