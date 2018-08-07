#!/usr/bin/python
# encoding=utf8

from redminelib import Redmine
from jinja2 import Environment, DictLoader
from collections import Counter
import re
import sys
import ClassUser
import Mysql
import Issue
import config
import argparse

reload(sys)
sys.setdefaultencoding('utf8')

class Redm:
    def __init__(self):
        self.redmine = self.auth_redmine_api()
        self.full_name_u = self.get_all_users()
        self.mysql = Mysql.MysqL()

    def auth_redmine_api(self):
        try:
            redmine = Redmine(config.REDMINE_URL, key=config.REDMINE_KEY)
            print("Auth complete\n")
            return  redmine
        except:
            sys.exit('Auth redmine failed!')

    def word_upper(self,string_d, type):
        if type == '1' or type == '4':  # firstname+lastname
            return re.findall(r'\b[A-Z]{1}[a-z]+\b', string_d)
        elif type == '2':  # email
            return re.findall(r'[a-zA-Z0-9]{1,50}\.[a-zA-Z0-9]{1,50}[@][a-z]{2,15}\.[a-z]{2,3}', string_d)
        elif type == '3' or type == '5':  # login
            return re.findall(r'[a-zA-Z]{1,50}[.]{1}[a-zA-Z]{1,50}', string_d)
        else:
            return []

    def get_all_users(self):
        users = self.redmine.user.all()
        list_user = []
        for u in users:
            for of in u.custom_fields:
                user = ClassUser.User(u.firstname, u.lastname, of.value, u.mail, u.id, u.login)
                list_user.append(user)
        return list_user

    def type_search(self, contain_user_str, t):
        result = []
        if t == '1':
            for us in self.full_name_u:
                if us.firstname in contain_user_str and us.lastname in contain_user_str:
                    result.append(us.firstname + " " + us.lastname)

        elif t == '2':
            for us in self.full_name_u:
                if us.mail in contain_user_str:
                    result.append(us.firstname + " " + us.lastname)
        elif t == '3':
            for us in self.full_name_u:
                if us.canonical_name in contain_user_str:
                    result.append(us.firstname + " " + us.lastname)
        elif t == '4':

            fl = True
            while fl:
                try:
                    determ = raw_input("1.Firstname\n2.Lastname\n3.First or Last\n4.Correct\n5.Exit\n")
                except:
                    print ("Error input")
                tmp = []
                if determ == '1':
                    for us in self.full_name_u:
                        if us.firstname in contain_user_str:
                            tmp.append(us.firstname + " " + us.lastname)
                            fl = False
                elif determ == '2':
                    for us in self.full_name_u:
                        if us.lastname in contain_user_str:
                            tmp.append(us.lastname + " " + us.firstname)
                            fl = False
                elif determ == '3':
                    for us in self.full_name_u:
                        if us.lastname in contain_user_str or us.firstname in contain_user_str:
                            tmp.append(us.firstname + " " + us.lastname)
                            fl = False
                elif determ =='4':
                    name = []
                    print ("After regular expression) ")
                    for u in contain_user_str:
                        print (u)
                    print ("\n")
                    try:
                        first = str(raw_input("Correct Firstname(Eugene):  "))
                        last = str(raw_input("Correct Lastname(Chistyakov):  "))
                        name.append(first)
                        name.append(last)
                        for us in self.full_name_u:
                            if us.firstname in name[0] and us.lastname in name[1]:
                                result.append(us.lastname + " " + us.firstname)
                        return result
                    except:
                        print ("Input error!")
                        return None

                elif determ == '5':
                    return result

            tmp.sort()
            for t in enumerate(tmp):
                print (str(t[0]) + " " + str(t[1]))

            e = True
            while (e):
                try:
                    a = int(raw_input('Num:\n'))
                    result.append(tmp[a])
                except:
                    print("Error input num!")
                try:
                    exit = raw_input("Exit?y/n\n")
                    if exit == 'y':
                        e = False
                except:
                    print"Error input exit!"

            return result

        else:
            print ('ups')
        return result

    def print_issue(self,issue):
        try:
            print ("Url:    " + issue.url)
            print ("Status:  " + str(issue.status))
            print ("Subject:  " + issue.subject)
            print ("Description:  " + issue.description)
            print ("Name of project:  " + str(issue.project))
            print ("Assigned to:  " + str(issue.assigned_to))
            print ("Author:  " + str(issue.author))
            for w in issue.watchers:
                print ("Watchers: " + str(w))
        except:
            print("Print error")

    def print_task_issue(self,issue, usr, scope, list_issue):
        Issue_print = Issue.TaskRedmine(issue, usr, scope)
        list_issue.append(Issue_print)

        print ('Scope:  ' + scope)
        print ("Redmine user id:  " + str(usr.redmine_id))
        print ('Canonical name:  ' + usr.canonical_name)
        print ("Email:  " + usr.mail)
        print ('Firstname:  ' + usr.firstname)
        print ('Lastname:  ' + usr.lastname)
        print ('Office:  ' + usr.office)
        try:
            print ("Assigned to:  " + str(issue.assigned_to))
        except:
            print("Print Assigned_to error")
        print ("Status:  " + str(issue.status))
        print ("Subject:  " + issue.subject)
        print ("Description:  " + issue.description)
        print ("Name of project:  " + str(issue.project))

        return list_issue

    def input_field_search(self):
        while True:
            s = raw_input('1 - description \n' + '2 - subject \n' + '3 - all \n' + '4 - exit\n')
            if s == '1' or s == '2' or s == '3' or s == '4':
                return s

    def confirm_db(self,usr,issue,scope):
        print("Confirm?")
        s = raw_input('-y?->')
        if s == 'y':
            print("Completed")
            self.mysql.mysqlConfirm(usr, issue, scope + 1)
        elif s == 'n':
            try:
                if usr.edit_task_user():
                    self.mysql.mysqlConfirm(usr, issue, scope + 1)
                else:
                    print ("Data wasn't uploaded because field task is not editing")
            except:
                print "Ups confirm to database"
        else:
            print ("Please,try again later y/n \n data wasn't uploaded")

    def get_describe_type(self,issue, field):
        list_issue = []
        list_issue_all = []
        str_field_low = ''
        str_field_origin = ''

        if field == '1':
            str_field_origin += issue.description
            str_field_low += issue.description.lower()
        elif field == '2':
            str_field_origin += issue.subject
            str_field_low += issue.subject.lower()
        elif field == '3':
            str_field_origin += issue.description
            str_field_origin += issue.subject
            str_field_low += str_field_origin.lower()
            heap_search = []
            filter = []

            try:
                for w in issue.watchers:
                    filter.append(self.redmine.user.filter(name=str(w)))
            except: print ("Watchers(")
            try:filter.append(self.redmine.user.filter(name=str(issue.author)))
            except: print ("Author( ")
            try: filter.append(self.redmine.user.filter(name=str(issue.assigned_to)))
            except: print ("Assigned(")

            for f in filter:
                for u in f:
                    for of in u.custom_fields:
                        office = of.value
                        usr = ClassUser.User(u.firstname, u.lastname, office, u.mail, u.id, u.login)
                        heap_search.append(usr)

            len = heap_search.__len__()
            count = 1
            for u in self.full_name_u:
                for h in heap_search:
                    if h.equal(u):
                        list_issue.append(u)
                        if count == len:
                            break
                        count =+ 1
        else:
            return None

        scope = 0
        strings_for_search_en = ['access to', 'vpn', 'sgx', 'git', 'svn']
        list_issue_res = []

        for str_s in strings_for_search_en:
            match = re.search(str_s, str_field_low)
            if match is not None:
                if field != '3':
                    print ("Type search:")
                    try:
                        t = raw_input("1.Firstname and Lastname\n2.Email\n3.Login \n4.Lastname or Firstname\n")
                    except:
                        sys.exit('Ups type_search')


                    contain_user_str = self.word_upper(str_field_origin, t)
                    users_task = self.type_search(contain_user_str,t)
                    if not users_task:
                        print ('Look list after regular expression: ' + str(contain_user_str))
                        print('users is not exist')
                        break

                    for us in users_task:
                        users_filt = self.redmine.user.filter(name=us)
                        office = ''
                        for u in users_filt:
                            for of in u.custom_fields:
                                office = of.value
                            usr = ClassUser.User(u.firstname, u.lastname, office, u.mail, u.id, u.login)
                            list_issue_res = self.print_task_issue(issue, usr, strings_for_search_en[scope], list_issue)
                            self.confirm_db(usr,issue,scope)

                    return list_issue_res

                else:
                    recomend = Counter(list_issue).most_common(1)
                    for rec in recomend:
                        print ("Repetitions  " + str(rec[1]))
                        rec[0].print_user()
                        r = raw_input("Ok?y/n\?\n")
                        if r == 'y':
                            list_issue_res = self.print_task_issue(issue,rec[0],strings_for_search_en[scope],list_issue_all)
                            self.confirm_db(rec[0],issue,scope)
                            return list_issue_res
                        elif r =='n':
                            list_count = Counter(list_issue)
                            for u in list_count:
                                print ("Repetitions  " + str(list_count[u]))
                                u.print_user()

                            try:
                                ex = raw_input("exit?y/n")
                                if ex == 'n':
                                    id_user = int(raw_input("Enter id user:  "))
                                    for u in list_issue:
                                        if u.redmine_id == id_user:
                                            self.confirm_db(u, issue, scope)
                                            break
                                    return list_issue
                                elif ex == 'y':return None
                            except:
                                print("Error input id")
                                return None
            scope += 1
        return None

    def get_describe_of_issue(self,numt):
        if self.redmine is not None:
            try:
                issue = self.redmine.issue.get(numt)
            except:
                sys.exit("Task is not exist!")
            self.print_issue(issue)

            if self.mysql.db is not None and self.full_name_u is not None:
                while True:
                    s = self.input_field_search()
                    list_issue = self.get_describe_type(issue, str(s))
                    if list_issue is None and s != '4':
                        print ('Not found ')
                        print ("Url:    " + issue.url + '\n')
                    else:
                        self.mysql.mysqlSelect()
                        break

            s = raw_input('Do you want to clear the database? y/n   ')
            if s == 'y':
                print ('1 - All \n2 - Task_id')
                try:
                    hd = raw_input()
                    if hd == '1':
                        self.mysql.mysqlClear()
                    elif hd == '2':
                        t = int(raw_input(':  '))
                        self.mysql.mysqlDelete(t)
                    else:
                        print ("1 or 2!")
                except:
                    print('input error')

            self.mysql.mysqlDisconnect()
            return list_issue
        else:
            print ("Redmine object is None")
            return None

    def reportHtml(self,list_task):
        res = []
        count = 0

        if len(list_task) > 0:
            for i in list_task:
                res.append([])
                res[count].append(str(i.issue.id))
                res[count].append(i.scope)
                res[count].append(str(i.user.redmine_id))
                res[count].append(i.user.canonical_name)
                res[count].append(i.user.mail)
                res[count].append(i.user.firstname)
                res[count].append(i.user.lastname)
                res[count].append((i.user.office))
                try:
                    res[count].append((i.issue.assigned_to))
                except:
                    print ("Error print assigned_to")
                    res[count].append("")
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

        with open("tasks.html", "w", ) as result:
            result.write(template.render(name=res, len=count_is, len_sub=count_sub_is))

    def create_parser_arg(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', type=int, help="Number of task redmine")
        parser.add_argument('-r', type=str, choices=['html'], help="Argument format (support html)")
        return parser

    def main(self):
        parser = self.create_parser_arg()
        namespace = parser.parse_args(sys.argv[1:])
        num = namespace.t
        rep = namespace.r

        if num is None:
            try:
                n = int(raw_input("Enter number of task: "))
                num = n
            except:
                sys.exit("Error input number task")

        list_task = self.get_describe_of_issue(num)

        if rep == "html" and list_task is not None:
            self.reportHtml(list_task)

if __name__ ==  '__main__':
    redmine_class = Redm()
    redmine_class.main()



