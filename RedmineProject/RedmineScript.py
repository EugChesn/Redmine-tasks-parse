from redminelib import Redmine
import re
import ClassUser
import Mysql
import config
global redmine
global full_name_u

def auth_redmine_api():
    try:
        redmine = Redmine(config.REDMINE_URL, key = config.REDMINE_KEY)
        print("Auth complete\n")
        return redmine
    except:
        print("Error auth")

def word_upper(string_d):
    temp_s = re.findall(r'[A-Z]\w+(?<!_)',string_d)
    return temp_s

def get_all_users():
    users = redmine.user.all()
    list_user = []
    for u in users:
        for of in u.custom_fields:
            user = ClassUser.User(u.firstname,u.lastname,of.value,u.mail,u.id,u.login)
            list_user.append(user)
    return list_user

def print_task_issue(issue,usr,scope):
    print ('Scope:  ' + scope)
    print ("Redmine user id:  " + str(usr.redmine_id))
    print ('Canonical name:  ' + usr.canonical_name)
    print ("Email:  " + usr.mail)
    print ('Firstname:  ' + usr.firstname)
    print ('Lastname:  ' + usr.lastname)
    print ('Office:  ' + usr.office)
    print ("Assigned to:  " + str(issue.assigned_to))
    print ("Status:  " + str(issue.status))
    print ("Subject:  " + issue.subject)
    print ("Description:  " + issue.description)
    print ("Name of project:  " + str(issue.project))

def input_field_search():
    while True:
        s = raw_input('1 - description \n' +'2 - subject \n' + '3 - exit \n')
        if s == '1' or s == '2' or s == '3':
            return s

def get_describe_type(issue,field,mysql):
    str_field_low = ''
    str_field_origin = ''

    if field == '1':
        str_field_origin += issue.description
        str_field_low += issue.description.lower()
    elif field == '2':
        str_field_origin += issue.subject
        str_field_low += issue.subject.lower()
    else:
        return None

    scope = 0
    strings_for_search_en = ['vpn','sgx','git','svn']

    for str_s in strings_for_search_en:
        match = re.search(str_s, str_field_low)
        if match is not None:
            contain_user_str = word_upper(str_field_origin)

            users_task = []
            for us in full_name_u:
                if us.firstname in contain_user_str and us.lastname in contain_user_str:
                    users_task.append(us.firstname + ' ' + us.lastname)

            if not users_task:
                print ('Look: ' + str(contain_user_str))
                print('users is not exist')
                break

            for us in users_task:
                users_filt = redmine.user.filter(name=us)
                office = ''
                for u in users_filt:
                    for of in u.custom_fields:
                        office = of.value
                    usr = ClassUser.User(u.firstname, u.lastname, office, u.mail, u.id, u.login)
                    print_task_issue(issue, usr, strings_for_search_en[scope])

                    print("Confirm?")
                    s = raw_input('-y?->')
                    if s == 'y':
                        print("Completed")
                        mysql.mysqlConfirm(usr, issue)
                    elif s == 'n':
                        try:
                            if usr.edit_task_user():
                                mysql.mysqlConfirm(usr, issue)
                            else:
                                print ("Data wasn't uploaded because field task is not editing")
                        except:
                            print "Ups confirm to database"
                    else:
                        print ("Please,try again later y/n \n data wasn't uploaded")
            return match
        else:
            return None

def get_describe_of_issue():
    if redmine is not None:
        mysql = Mysql.MysqL()
        print('Task> ')
        numt = int(input())

        try:
            issue = redmine.issue.get(numt)
        except:
            print("Error, task is not exist")

        if mysql.db is not None and full_name_u is not None:
            while True:
                s = input_field_search()
                if get_describe_type(issue,str(s),mysql) is None and s!='3':
                    print ('Not found scope \n')
                else:
                    break
    else:
        print ("Redmine object is None")

redmine = auth_redmine_api()
full_name_u = get_all_users()
get_describe_of_issue()


