import RedmineScript
from jinja2 import Environment, DictLoader

RedmineScript.Run()
res = RedmineScript.result

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
    <tr>
    <th>{{name[0]}}</th><th>{{name[1]}}</th><th>{{name[2]}}</th><th>{{name[3]}}</th><th>{{name[4]}}</th><th>{{name[5]}}</th><th>{{name[6]}}</th><th>{{name[7]}}</th><th>{{name[8]}}</th><th>{{name[9]}}</th><th>{{name[10]}}</th><th>{{name[11]}}</th><th>{{name[12]}}</th>
   </table>
  </body>
</html>
'''

env = Environment(loader=DictLoader({'index.html': html}))
template = env.get_template('index.html')

f = open ("index.html" , 'w')
f.write(template.render(name= res))
f.close()
