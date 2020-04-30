#!/usr/bin/env python3

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
        res = enxo(urlo[14:], urlo[8:14], 1)
  
  def enxo(self, n, y, z):
    o = ''
    chr1, chr2, chr3 = '', '', ''
    enc = []
    revo = []
    for i in range(65):
      revo[ doc[i] ] = i
    for ( my $i = 0; $i < 65; $i++ ) {
        $revo[ $doc[$i] ] = $i;
    }
    """
    my ( $n, $y, $z ) = @_;
    
    my $i = 0;
    if ( $z == 1 ) {
        do {
            for ( my $j = 0; $j < 4; $j++ ) {
                $enc[$j] = $revo[ charCodeAt( $n, $i++ ) ];
            }
            $chr1 = ( $enc[0] << 2 ) | ( $enc[1] >> 4 );
            $chr2 = ( ( $enc[1] & 15 ) << 4 ) | ( $enc[2] >> 2 );
            $chr3 = ( ( $enc[2] & 3 ) << 6 ) | $enc[3];
            $o = $o . chr($chr1);
            $o = $o . chr($chr2) if $enc[2] ne 64;
            $o = $o . chr($chr3) if $enc[3] ne 64;
        } while ( $i < length($n) );
        $n = $o;
    }
    my $result = '';
    for ( my $i = 0; $i < length($n); ++$i ) {
        $result
            .= chr(
            ord( substr( $y, $i % length($y), 1 ) ) ^
                ord( substr( $n, $i, 1 ) ) );
    }
    if ( $z == 1 ) {
        $o = $result;
    }

    $i = 0;
    if ( $z == 0 ) {
        $n = $result;
        do {
            my $chr1 = charCodeAt( $n, $i++ );
            my $chr2 = charCodeAt( $n, $i++ );
            my $chr3 = charCodeAt( $n, $i++ );
            $enc[0] = $chr1 >> 2;
            $enc[1] = ( ( $chr1 & 3 ) << 4 ) | ( $chr2 >> 4 );
            $enc[2] = ( ( $chr2 & 15 ) << 2 );
            if ( defined $chr3 ) {
                $enc[2] = $enc[2] | ( $chr3 >> 6 );
                $enc[3] = $chr3 & 63;
            }
            if ( !isNumeric($chr2) ) {
                $enc[2] = $enc[3] = 64;
            }
            elsif ( !isNumeric($chr3) ) {
                $enc[3] = 64;
            }
            for ( my $j = 0; $j < 4; $j++ ) {
                $o .= chr( $doc[ $enc[$j] ] );
            }
        } while ( $i < length($n) );
    }
    return $o;
    """
    return ""

user_ref = user()
user_ref.get_citycode()
user_ref.validatio()
user_ref.initial()
user_ref.agir()
