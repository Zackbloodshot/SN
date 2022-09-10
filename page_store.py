from Sagiri_Notifs import REDIS 

#
def exists(name):
    check = REDIS.exists(name)
    if check == 1:
        return True
    else:
        return False

def store(name, link):
  REDIS.set(name, link)
  
def get_stored(name):
  return ret(REDIS.get(name))
  
def ret(redis_string):
  try:
    red = redis_string.decode('UTF-8')
    return red
  except:
    return ""
