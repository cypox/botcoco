import os
from datetime import datetime
import shlex, subprocess
import shutil
import filecmp
import urllib.request
import http

debug = True
def print_debug(msg, echo = debug):
  if echo:
    print("[{}] {}".format(datetime.now().strftime("%H:%M"), msg))

class pseudo:
  def __init__(self, name, timestamp = ''):
    self.name = name
    if timestamp == '':
      self.timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M")
    else:
      self.timestamp = timestamp

class person:
  def __init__(self):
    self.pseudos = []
    self.age = ''
    self.city = ''
    self.uid = ''
    self.constructor = ''
    self.online_name = ''

  def from_log(self, line):
    self.constructor = line
    items = line.split('!')
    items = [x[1:-1] for x in items]
    self.online_name = items[1].rstrip()
    self.pseudos.append(pseudo(self.online_name))
    self.age = items[3]
    self.city = items[4]
    self.uid = items[5]

  def from_db(self, uid, names, age, city):
    self.pseudos = [pseudo(x.split('|')[0], x.split('|')[1]) for x in names.split(',')]
    self.online_name = self.pseudos[-1].name
    self.age = age
    self.uid = uid
    self.city = city
  
  def add_name(self, name):
    if self.pseudos[-1].name != name:
      self.pseudos.append(pseudo(name))
  
  def get_line(self):
    all_names = ''.join([x.name+'|'+x.timestamp+',' for x in self.pseudos])
    all_names = all_names[:-1]
    return '{};{};{};{}\n'.format(self.uid, all_names, self.age, self.city)
  
  def download_update_file_v2(self):
    try:
      link = "https://pix1.coco.fr/{}".format(self.uid)
      req = urllib.request.Request(link, headers={'User-agent':'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0'})
      resp = urllib.request.urlopen(req)
    except http.client.RemoteDisconnected:
      return
    temp_filename = 'avatars/TEMP-{}'.format(self.uid)
    with open(temp_filename, "wb") as fd:
      fd.write(resp.read())
    if filecmp.cmp('avatars/coco.jpg', temp_filename):
      os.remove(temp_filename)
      return
    if int(resp.getheader('Content-Length')) < 10:
      os.remove(temp_filename)
      return
    content_type = resp.getheader('Content-Type').split('/')[1]
    i = 0
    filename = "avatars/{}-{:03d}.{}".format(self.uid, i, content_type)
    exist = False
    while os.path.isfile(filename):
      exist = exist or filecmp.cmp(filename, temp_filename)
      i += 1
      filename = "avatars/{}-{:03d}.{}".format(self.uid, i, content_type)
    if not exist:
      if i == 0:
        print_debug('downloading file {} for user {}'.format(filename, self.online_name))
      else:
        print_debug('updating file {} for user {}'.format(filename, self.online_name))
      shutil.move(temp_filename, filename)
    else:
      os.remove(temp_filename)

  def download_update_file_v1(self):
    link = "https://pix1.coco.fr/{}".format(self.uid)
    temp_filename, headers = urllib.request.urlretrieve(link)
    if filecmp.cmp('avatars/coco.jpg', temp_filename):
      os.remove(temp_filename)
      return
    if int(headers['Content-Length']) < 10:
      os.remove(temp_filename)
      return
    content_type = headers['Content-Type'].split('/')[1]
    i = 0
    filename = "avatars/{}-{:03d}.{}".format(self.uid, i, content_type)
    exist = False
    while os.path.isfile(filename):
      exist = exist or filecmp.cmp(filename, temp_filename)
      i += 1
      filename = "avatars/{}-{:03d}.{}".format(self.uid, i, content_type)
    if not exist:
      if i == 0:
        print_debug('downloading file {} for user {}'.format(filename, self.online_name))
      else:
        print_debug('updating file {} for user {}'.format(filename, self.online_name))
      shutil.move(temp_filename, filename)
    else:
      os.remove(temp_filename)


class person_db:
  def __init__(self):
    self.users = []
  
  def add_update(self, user):
    p = self.find(user)
    if p == -1:
      print_debug('new user found: {}'.format(user.online_name))
      self.users.append(user)
    else:
      self.users[p].add_name(user.online_name)
      if self.users[p].online_name != user.online_name:
        print_debug('user {} updated her name to {}'.format(self.users[p].online_name, user.online_name))
        pass
  
  def add(self, user):
    self.users.append(user)
  
  def load_file(self, db_file):
    if os.path.isfile(db_file):
      with open(db_file, 'r') as f:
        for line in f:
          line = line.rstrip()
          if line != '':
            ps = line.split(';')
            p = person()
            p.from_db(ps[0], ps[1], ps[2], ps[3])
            self.add(p)
  
  def to_file(self, db_file):
    with open(db_file+'_temp', 'w') as f:
      for p in self.users:
        f.write(p.get_line())
    shutil.move(db_file+'_temp', db_file)

  def count(self):
    return len(self.users)
  
  def find(self, user):
    for i in range(len(self.users)):
      if self.users[i].uid == user.uid and self.users[i].age == user.age and self.users[i].city == user.city:
        return i
    return -1

command_line = '/home/miloslav/botcoco/cocoweb/cocoweb.pl -s W -a list'

db_file = 'users_db'

# reading online users from bot
args = shlex.split(command_line)
proc = subprocess.Popen(args, stdout=subprocess.PIPE)

output = proc.stdout.read().decode()
lines = output.split('\n')
while("" in lines) : 
  lines.remove("") 

online_people = []
for line in lines:
  if line[0] == '!':
    p = person()
    p.from_log(line)
    online_people.append(p)
print_debug('found {} users online.'.format(len(online_people)))

# reading database file
db_users = person_db()
db_users.load_file(db_file)
previous_count = db_users.count()
print_debug('found {} users in database.'.format(db_users.count()), echo=True)

# updating database file
for op in online_people:
  db_users.add_update(op)
  op.download_update_file_v2()

db_users.to_file(db_file)
new_count = db_users.count()
print_debug('added {} new users.'.format(new_count-previous_count), echo=True)
