#!/usr/bin/python

import sys, os, re
import MySQLdb as mdb
from subprocess import PIPE, Popen

USAGE = \
'''
This script, can
1) extracts weibo of uid
2) segment the words(using bamboo), and map word to id
  the output file will be with .seg suffix
  word_id.txt will record the map relatonship
  note:
    @xxx
    [xxx]
    //@xxx:
    !!!
    ...

USAGE:
python preprocess.py extract uid out_dir
python3 preprocess.py segment input_list
'''

HOST = 'localhost'
USER = 'root'
PASSWD = 'google'
DB = 'weibo_xinli_500'
TABLE = 'sina_statuses'
FIELDS = ('created_at', 'text')

WORD_ID = 'word_id.txt'
word_id = {}


##################################################

def init_word_id(f):
  if os.path.exists(f):
    for line in open(f):
      line = line.strip()
      if not line:  # ignore empty line
        continue
      line = line.split('\t')
      word_id[line[0]] = int(line[1])

def save_word_id():
  with open(WORD_ID, 'w') as out:
    for w, d in word_id:
      out.write('%s\t%d\n' % (w, d))

def add_word(w):
  # if not w:
  #   return -1
  return word_id.setdefault(w, len(word_id))

##################################################

def fetch(u):
  rows = []
  with mdb.connect(HOST, USER, PASSWD, DB, charset='utf8') as cur: # not conn
    # cur = conn.cursor()
    # where user_id = %s limit 10
    cur.execute('select %s, %s from %s where user_id = %d' % \
                (FIELDS + (TABLE, u)))
    rows = cur.fetchall()
    # do I need to transform the date?
    '''
    for r in rows:
      print(r[1].encode('utf-8'))  # need to convert unicode to bytes
    '''
    # change datetime.datetime to str
    rows = [(str(r[0]), r[1]) for r in rows]

  return rows

#################################################

def bamboo(text):
  proc = Popen('bamboo', stdin=PIPE, stdout=PIPE)
  out = proc.communicate(input=text.encode())[0].decode()
  out = out.split()
  for ix, s in enumerate(out):
    # remove begining/ending '.[]/'
    while s and s[-1] in '.[]/':
      s = s[:-1]
    while s and s[0] in '.[]/':
      s = s[1:]
    out[ix] = s
  return ' '.join(out)

# I treat each weibo/line as a sentence
def segment(f):
  if not os.path.exists(f):
    sys.stderr.write('file %s not exists.' % f)
    return

  PUNC = set('!?！？。')
  # .
  # be careful about '-', since it DELIMITERS will be used in [DELIMITERS]
  DELIMITERS = ' \-~,;:\'"{}' + \
               '；﹔︰﹕：，﹐、．﹒˙·～‥‧′〃〝〞‵‘’『』「」“”'

  word_text = ''
  id_text = ''
  for line in open(f):
    line = line.strip()
    if not line:
      continue
    # find special substr:
    # @xxx
    # !!!
    # //@xxx:
    # [xxx]
    word_lst = []
    id_lst = []

    def push_word(w):
      if not w: return
      word_lst.append(w)
      id_lst.append(add_word(w))

    def push_str(str):
      if not str: return
      for s in bamboo(str).split():
        push_word(s)

    for clip in re.split('['+DELIMITERS+']', line):
      if not clip: continue
      # print(clip)
      last_str = ''
      for ix, c in enumerate(clip):
        # xxx!!
        if c in PUNC:
          if last_str:
            push_str(last_str)
            last_str = ''
          push_word(c)
        # xxx//@xx
        elif c == '@':
          if ix >= 2 and clip[ix-2:ix] == '//':
            push_str(clip[:ix-2])
            push_word('//')
          else:
            push_str(clip[:ix])
          push_word(clip[ix:])
          last_str = ''
          break
        elif c == '[':
          push_str(clip[:ix])
          last_str = c
        elif c == ']' and last_str:
          if last_str[0] == '[':
            push_word(last_str + ']')
            last_str = ''
          else:
            push_str(last_str)
            last_str = ''
        else:
          last_str += c

      if last_str:
        push_str(last_str)

      # print(word_lst)

    word_text += ' '.join(word_lst) + '\n'
    id_text += ' '.join(str(x) for x in id_lst) + '\n'

  open(f + '.seg', 'w').write(word_text)
  open(f + '.id', 'w').write(id_text)

if __name__ == '__main__':
  # extract uid out_dir
  if len(sys.argv) == 4 and sys.argv[1] == 'extract':
    uid = [int(line) for line in open(sys.argv[1])]
    out_dir = sys.argv[2]
    if not os.path.isdir(out_dir):
      os.mkdir(out_dir)

    for u in uid:
      rows = fetch(u)
      with open(out_dir + '/' + str(u), 'w') as out:
        for d, t in rows:
          # out.write(d + '\t' + t.encode('utf8') + '\n')
          out.write(t.encode('utf8') + '\n')

  # segment file in input_list
  elif len(sys.argv) == 3 and sys.argv[1] == 'segment':
    if sys.version.title()[0] != '3':
      print('For convinence, you should use python3 for segment')
      exit(1)

    init_word_id(WORD_ID)
    input_list = open(sys.argv[2])
    for f in input_list:
      f = f.strip()
      if not f or not os.path.exists(f):
        continue
      segment(f)
    save_word_id()

  else:
    print(USAGE)
    exit(1)




