user = '634159885'
avatar = 'WKUZEXXZKWEOTOKREXWQ'

from urllib.request import urlopen
import re
import random
import math

class cookie:
  def __init__(self):
    self.coda = None
    self.samedi = None

class user:
  def __init__(self):
    self.login = 'Fianso'
    self.age = 40
    self.sex = 1
    self.zip = '59300'
    self.cookav = math.floor (random.randint(0, 890000000) + 100000000)
    self.referenz = 0
    self.speco = 0
    self.mynickID = '999999'
    self.monpass = 0
    self.roulix = 0
    self.sauvy = ''
    self.cookies = cookie()

    self.myavatar = ''
    self.mypass = ''
    self.ifravatar = ''

    self.citydio = ''
    self.townzz = ''

    self.my_port = 80
    self.url1 = 'http://cloud.coco.fr/'
  
  def get_citycode(self):
    if len(self.zip) != 5:
      print('incorrect zip code')
      exit()
    if self.zip[0] == '0':
      self.zip = self.zip[1:]
    
    url = 'http://www.coco.fr/cocoland/' + self.zip + '.js'
    response = urlopen(url)
    result = response.read().decode()

    regex = re.compile('([0-9]+\*.+\*)+')
    if not regex.search(result):
      print('result cannot be decoded:\nBEGIN RESULT:\n{}\nEND RESULT'.format(result))
      exit()

    citycode = regex.search(result).group()
    city_codes = citycode.split('*')
    codes = city_codes[::2]
    cities = city_codes[1::2]
    if len(cities) > 1:
      ind = random.randint(0, len(cities)-1)
      self.citydio = codes[ind]
      self.townzz = cities[ind]
    else:
      self.citydio = codes[0]
      self.townzz = cities[0]
  
  def validatio(self):
    citygood = '{:0>5}'.format(self.citydio)
    self.inform = '{}#{}#{}#{}#{}#0#{}#'.format(self.login, self.sex, self.age, self.townzz, citygood, self.cookav)
    self.cookies.coda = self.inform

    if len(self.sauvy) < 2:
      self.sauvy = self.cookav
  
  def initial(self):
    if self.cookies.samedi is not None:
      infor = self.cookies.samedi
      avatar = infor[0:9]
      _pass = infor[9:29]
    else:
      avatar = random.randint(0, 890000000) + 100000000
      _pass = ''
    self.myavatar = avatar
    self.mypass = _pass
    self.infor = '{}{}'.format(self.myavatar, self.mypass)
    self.cookies.samedi = self.infor
    self.ifravatar = 'ava5.html?log={}'.format(self.myavatar)
    print('ifravatar: {}'.format(self.ifravatar))
  
  def agir(self, text=None):
    if text is None:
      text = '40{}*{}{}{}{}{}'.format(self.login, self.age, self.sex, self.citydio, self.myavatar, self.mypass)
    url = '{}{}'.format(self.url1, text)
    print(url)
    response = urlopen(url)
    result = response.read().decode()
    regex_func = re.compile('[a-z1]+')
    regex_parm = re.compile('\'.*\'')
    function = regex_func.search(result).group()
    parameter = regex_parm.search(result).group()[1:-1]
    self.process1(parameter)
  
  def process1(self, urlu):
    urlo = urlu
    hzy = urlo.index('#')
    urlo = urlo[hzy+1:]
    
    firstchar = urlo[0]
    molki = ord(urlo[0])
    self.process_int(urlo)
  
  def process_int(self, urlo):
    olko = int(urlo[0:2])
    if olko == 15:
      tkt = urlo[2:8]
      if int(tkt) < 900000:
        self.mynickID = tkt
        self.monpass = urlo[8:14]



user_ref = user()
user_ref.get_citycode()
user_ref.validatio()
user_ref.initial()
user_ref.agir()
