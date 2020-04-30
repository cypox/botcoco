import shlex, subprocess

class person:
  def __init__(self):
    self.name = ''
    self.age = ''
    self.city = ''
    self.uid = ''
    self.constructor = ''

  def from_log(self, line):
    self.constructor = line
    items = line.split('!')
    self.name = items[1]
    self.age = items[3]
    self.city = items[4]
    self.uid = items[5]

  def from_db(self, uid, name, age, city):
    self.name = name
    self.age = age
    self.uid = uid
    self.city = city
  
  def get_line(self):
    return '{},{},{},{}\n'.format(self.uid, self.name, self.age, self.city)

class person_db:
  def __init__(self):
    self.users = []
  
  def add(self, user):
    self.users.append(user)
  
  def count(self):
    return len(self.users)
  
  def exist(self, user_id):
    for p in self.users:
      if p.uid == user_id:
        return True
    return False

command_line = '/mnt/c/Users/Miloslav/Desktop/botcoco/cocobot/cocoweb.pl -s W -a list'

db_file = 'users_db'

args = shlex.split(command_line)

proc = subprocess.Popen(args, stdout=subprocess.PIPE)

output = proc.stdout.read()
lines = output.split('\n')
while("" in lines) : 
  lines.remove("") 

online_people = []
for line in lines:
  #print(line)
  if line[0] == '!':
    p = person()
    p.from_log(line)
    online_people.append(p)

print('Found {} users online.'.format(len(online_people)))

db_users = person_db()
with open(db_file, 'r') as f:
  for line in f:
    line = line.rstrip()
    if line != '':
      #print('line = {}'.format(line))
      ps = line.split(',')
      p = person()
      p.from_db(ps[0], ps[1], ps[2], ps[3])
      #print(p.get_line())
      db_users.add(p)

print('Found {} users in database.'.format(db_users.count()))

added = 0
with open(db_file, 'a') as f:
  for op in online_people:
    #print('checking for {}'.format(op.uid))
    if not db_users.exist(op.uid):
      db_users.add(op)
      added += 1
      f.write(op.get_line())

print('Added {} new users.'.format(added))
