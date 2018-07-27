#!/usr/bin/python
from redminelib import Redmine
from jinja2 import Environment, DictLoader
import re
import sys
import ClassUser
import Mysql
import Issue
import config
import argparse

global list_issue
list_issue = []


def auth_redmine_api():
    try:
        redmine = Redmine(config.REDMINE_URL, key = config.REDMINE_KEY)
        print("Auth complete\n")
        return redmine
    except:
        print("Error auth")

def word_upper(string_d):
    temp_s = re.findall(r'\b[A-Z]{1}[a-z]+\b',string_d)
    return temp_s

def get_all_users():
    users = redmine.user.all()
    list_user = []
    for u in users:
        for of in u.custom_fields:
            user = ClassUser.User(u.firstname,u.lastname,of.value,u.mail,u.id,u.login)
            list_user.append(user)
    return list_user

def print_task_issue(issue,usr,scope,list_issue):
    Issue_print = Issue.TaskRedmine(issue,usr,scope)
    list_issue.append(Issue_print)

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
        print ('Description of task '+ str(issue.id) + ':  ' + str_field_origin)
        str_field_low += issue.description.lower()
    elif field == '2':
        str_field_origin += issue.subject
        print ('Subject of task ' + str(issue.id) + ':  ' + str_field_origin)
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
                print ('Look list after regular expression: ' + str(contain_user_str))
                print('users is not exist')
                break

            for us in users_task:
                users_filt = redmine.user.filter(name=us)
                office = ''
                for u in users_filt:
                    for of in u.custom_fields:
                        office = of.value
                    usr = ClassUser.User(u.firstname, u.lastname, office, u.mail, u.id, u.login)
                    print_task_issue(issue, usr, strings_for_search_en[scope],list_issue)
                    print("Confirm?")
                    s = raw_input('-y?->')
                    if s == 'y':
                        print("Completed")
                        mysql.mysqlConfirm(usr,issue,scope+1)
                    elif s == 'n':
                        try:
                            if usr.edit_task_user():
                                mysql.mysqlConfirm(usr, issue,scope+1)
                            else:
                                print ("Data wasn't uploaded because field task is not editing")
                        except:
                            print "Ups confirm to database"
                    else:
                        print ("Please,try again later y/n \n data wasn't uploaded")
            return match

        scope += 1
    return None

def get_describe_of_issue(numt):
    mysql = Mysql.MysqL()
    if redmine is not None:
        try:
            issue = redmine.issue.get(numt)
        except:
            print("Error, task is not exist")
            raise SystemExit

        if mysql.db is not None and full_name_u is not None:
            while True:
                s = input_field_search()
                if get_describe_type(issue,str(s),mysql) is None and s!='3':
                    print ('Not found \n')
                else:
                    mysql.mysqlSelect()
                    break

        s = raw_input('Do you want to clear the database? y/n   ')
        if s == 'y':
            print ('1 - All \n2 - Task_id')
            hd = raw_input()
            if hd == '1':
                mysql.mysqlClear()
            elif hd == '2':
                t = int(raw_input(':  '))
                mysql.mysqlDelete(t)

        mysql.mysqlDisconnect()

    else:
        print ("Redmine object is None")

def reportHtml():
    res = []
    count = 0

    if len(list_issue) > 0:
        for i in list_issue:
            res.append([])
            res[count].append(str(i.issue.id))
            res[count].append(i.scope)
            res[count].append(str(i.user.redmine_id))
            res[count].append(i.user.canonical_name)
            res[count].append(i.user.mail)
            res[count].append(i.user.firstname)
            res[count].append(i.user.lastname)
            res[count].append(str(i.user.office))
            res[count].append(str(i.issue.assigned_to))
            res[count].append(str(i.issue.status))
            res[count].append(i.issue.subject)
            res[count].append(i.issue.description)
            res[count].append(str(i.issue.project))

            count += 1

        count_is = len(res)
        count_sub_is = len(res[0])

    html = '''<!DOCTYPE html>
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      </head>
      <body>
       <table border="1" width="100%" cellpadding="5">
       <tr>
       <th>Id task </th><th>Scope</th><th>User id</th><th>Canonical name</th><th>Email</th><th>Firstname</th><th>Lastname</th><th>Office</th><th>Assigned to</th><th>Status</th><th>Subject</th><th>Description</th><th>Name Progect</th>
        </tr>
        {% for i in range(len) %}
        <tr>
            {% for j in range(len_sub) %}
            <th>{{name[i][j]}}</th>
            {% endfor %}
        </tr>
        {% endfor %}
       </table>
      </body>
    </html>
    '''

    env = Environment(loader=DictLoader({'index.html': html}))
    template = env.get_template('index.html')

    f = open("index.html", 'w')
    f.write(template.render(name=res, len=count_is, len_sub=count_sub_is))
    f.close()

def create_parser_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',type = int)
    parser.add_argument('-r',nargs='?',type = str,default = "html")
    return parser

if __name__ ==  '__main__':
    parser = create_parser_arg()
    namespace = parser.parse_args(sys.argv[1:])
    num = namespace.t
    rep = namespace.r

    global redmine
    global full_name_u
    redmine = auth_redmine_api()
    full_name_u = get_all_users()
    get_describe_of_issue(num)

    if rep == "html":
        reportHtml()



