from redminelib import Redmine
import re
import ClassUser
import Task
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
        user = ClassUser.User(u.firstname,u.lastname)
        list_user.append(user)
    return list_user

def get_describe_of_issue():
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
                for u in users_filt:
                    task = Task.Task(strings_for_search_en[scope],str(u.id),u.login,u.firstname,u.lastname,str(issue.assigned_to),u.mail,str(issue.status),subject,description,str(issue.project))
                    task.print_task()

                    print("Confirm?")
                    s = raw_input('-y?->')
                    if s =='y':
                        print("Completed")
                        mysql.mysqlConfirm(task,numt)
                    elif s =='n':
                        try:
                            print("Enter field for change: ")
                            field = str(input())
                            print("Enter value of field: ")
                            val = str(input())
                            task.edit_task(field,val)
                            mysql.mysqlConfirm(task,numt)
                        except:
                            print "Ups"

        elif match_d is not None:
            temp_str2 = word_upper(issue.description)
            contain_user_str2 = temp_str2.split(' ')

            users_task2 = []
            for us in full_name_u:
                if us.firstname in contain_user_str2 and us.lastname in contain_user_str2:
                    users_task2.append(us.firstname + ' ' + us.lastname)

            if not users_task2:
                print('users is not exist')
                break

            for us in users_task2:
                users_filt = redmine.user.filter(name = us)
                for u in users_filt:
                    task = Task.Task(strings_for_search_en[scope], str(u.id), u.login, u.firstname, u.lastname,str(issue.assigned_to), u.mail, str(issue.status), subject, description,str(issue.project))
                    task.print_task()

                    print("Confirm?")
                    s = raw_input('-y?->')
                    if s == 'y':
                        print("Completed")
                    elif s == 'n':
                        try:
                            print("Enter field for change: ")
                            field = str(input())
                            print("Enter value of field: ")
                            val = str(input())
                            task.edit_task(field, val)
                            mysql.mysqlConfirm(task,numt)
                        except:
                            print "Ups"
        else:
            print('task is not about vpn')
            break
        scope += 1
        break
    mysql.db.close()

redmine = auth_redmine_api()
get_describe_of_issue()

print("bye")
