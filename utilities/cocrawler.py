from urllib.request import urlopen
import sys
import re
import random
import math

def read_zip_db(zip_file):
  zips = dict()
  with open(zip_file, 'r') as f:
    for line in f:
      zip_code = line.split(' ', 1)[0]
      city_codes = line.split(' ', 1)[1][:-1]
      city_codes = city_codes.split('*')
      while '' in city_codes:
        city_codes.remove('')
      
      codes = city_codes[ ::2]
      names = city_codes[1::2]
      assert(len(codes) == len(names))

      for i in range(len(codes)):
        key = int(codes[i])
        value = (names[i], int(zip_code))
        zips[key] = value
  return zips

zips = read_zip_db('zips.txt')

class person:
  def __init__(self, text):
    self.age = int(text[0:2])
    self.sex = 'Male' if text[2] == '1' else 'Female'
    self.city = zips[int(text[3:8])][0]
    self.id = int(text[8:14])
    self.niv = text[14]
    self.stat = text[15]
    self.ok = text[16]
    self.name = text[17:]
  
  def __str__(self):
    return 'Name: {}\nAge : {}\nSex : {}\nCity: {}\nAvtr: {}\n'.format(self.name, self.age, self.sex, self.city, self.id)
  
  def __repr__(self):
    return 'Name: {}\nAge : {}\nSex : {}\nCity: {}\nAvtr: {}\n'.format(self.name, self.age, self.sex, self.city, self.id)

# me = person('29123495 ')
prefix = 'http://cloud.coco.fr/'
action = '10'
uid = '333116'
password = 'mvypPu'
gender = '0'
age = '0'

url = '{}{}{}{}{}{}'.format(prefix, action, uid, password, gender, age)
response = urlopen(url)
result = response.read().decode()

regex = re.compile('\'.*\'')
users_string = regex.search(result).group()

users = users_string[1:-1].split('#')
while '' in users:
  users.remove('')
response_id = users[0][0:2]
users[0] = users[0][2:]

user_refs = []
for u in users:
  new_user = person(u)
  user_refs.append(new_user)

print(user_refs)

prefix = 'http://cloud.coco.fr/'
action = '99'
uid = '333116'
password = 'mvypPu'
other_uid = '327798'
other_uid = uid
roulix = '1'
message = 'salut'

url = '{}{}{}{}{}{}'.format(prefix, action, uid, password, other_uid, roulix, message)
response = urlopen(url)
result = response.read().decode()
print(result)
