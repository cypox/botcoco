import os
import datetime
import shlex, subprocess
import shutil
import filecmp
import urllib.request

# download images for database
#for user in db_users.users:# use this if you want a full db picture download
for uid in range(100000, 1000000):
  link = "http://pix1.coco.fr/{}".format(uid)
  temp_filename, headers = urllib.request.urlretrieve(link)
  if int(headers['Content-Length']) < 10:
    continue
  content_type = headers['Content-Type'].split('/')[1]
  filename = "all_avatars/{}.{}".format(uid, content_type)
  if os.path.isfile(filename):
    if filecmp.cmp(filename, temp_filename):
      continue
    duplicate = False
    i = 1
    filename = "all_avatars/{}-{}.{}".format(uid, i, content_type)
    while os.path.isfile(filename):
      if filecmp.cmp(filename, temp_filename):
        duplicate = True
      i += 1
      filename = "all_avatars/{}-{}.{}".format(uid, i, content_type)
    if not duplicate:
      print('[{}] updating file {}'.format(datetime.datetime.now(), filename))
    shutil.move(temp_filename, filename)
  else:
    print('[{}] downloading file {}'.format(datetime.datetime.now(), filename))
    shutil.move(temp_filename, filename)
