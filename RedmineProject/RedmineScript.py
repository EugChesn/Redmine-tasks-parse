from redminelib import Redmine
import re
import ClassUser
import Mysql
import config
global redmine

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

def get_describe_of_issue():
    if redmine is not None:
        mysql = Mysql.MysqL()
        full_name_u = get_all_users()
        print('Task> ')
        numt = int(input())
        try:
            issue = redmine.issue.get(numt)
        except:
            print("Error, task is not exist")

        description = issue.description.lower()
        subject = issue.subject.lower()

        scope = 0
        strings_for_search_en = ['vpn','vpn access','create vpn','grant access vpn']

        for str_s in strings_for_search_en:
            match_d = re.search(str_s,description)
            match_s = re.search(str_s,subject)
            if match_s is not None:
                temp_str = word_upper(issue.subject)
                contain_user_str = temp_str

                users_task = []
                for us in full_name_u:
                    if us.firstname in contain_user_str and us.lastname in contain_user_str:
                        users_task.append(us.firstname + ' ' + us.lastname)

                if not users_task:
                    print('users is not exist')
                    break

                for us in users_task:
                    users_filt = redmine.user.filter(name = us)
                    office = ''
                    for u in users_filt:
                        for of in u.custom_fields:
                            office = of.value
                        usr = ClassUser.User(u.firstname,u.lastname,office,u.mail,u.id,u.login)
                        print_task_issue(issue, usr, strings_for_search_en[scope])

                        print("Confirm?")
                        s = raw_input('-y?->')
                        if s =='y':
                            print("Completed")
                            mysql.mysqlConfirm(usr,numt)
                        elif s =='n':
                            try:
                                if usr.edit_task_user():
                                    mysql.mysqlConfirm(usr,numt)
                                else: print ("Data wasn't uploaded because field task is not editing")
                            except:
                                print "Ups"
                        else:
                            print ("Please,try again later y or n \n data wasn't uploaded")

            elif match_d is not None:
                temp_str2 = word_upper(issue.description)
                contain_user_str2 = temp_str2

                users_task2 = []
                for us in full_name_u:
                    if us.firstname in contain_user_str2 and us.lastname in contain_user_str2:
                        users_task2.append(us.firstname + ' ' + us.lastname)

                if not users_task2:
                    print('users is not exist')
                    break

                for us in users_task2:
                    users_filt = redmine.user.filter(name = us)
                    office = ''
                    for u in users_filt:
                        for of in u.custom_fields:
                            office = of.value
                        usr = ClassUser.User(u.firstname,u.lastname,office,u.mail,u.id,u.login)
                        print_task_issue(issue, usr, strings_for_search_en[scope])

                        print("Confirm?")
                        s = raw_input('-y?->')
                        if s == 'y':
                            mysql.mysqlConfirm(usr, numt)
                        elif s == 'n':
                            try:
                                if usr.edit_task_user():
                                    mysql.mysqlConfirm(usr,numt)
                                else: print ("Data wasn't uploaded because field task is not editing")
                            except:
                                print "Ups"
                        else:
                            print ("Please,try again later y or n \n data wasn't uploaded")
            else:
                print('task is not about vpn')
                break
            scope += 1
            break

        mysql.mysqlSelect()
        mysql.db.close()
    else:
        print ("Redmine object is None")

redmine = auth_redmine_api()
get_describe_of_issue()


