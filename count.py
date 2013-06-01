
import os, sys
import collections

USAGE = \
'''This script map word to id, and count DF, id start from 1

Usage:
python3 count.py list
count DF, here doc is a weibo'''

ID_WORD = 'id_word.txt'
WORD_COUNT = 'id_word_count.txt'

word_id = {}
word_count = collections.defaultdict(int)

def init_word_id():
  for line in open(ID_WORD):
    line = line.strip().split('\t')
    assert line[1] not in word_id, line
    word_id[line[1]] = int(line[0])

def save_word_id():
  out = open(ID_WORD, 'w')
  for (w, d) in word_id.items():
    out.write('%d\t%s\n' % (d, w))

def save_word_count():
  out = open(WORD_COUNT, 'w')
  for (w, d) in word_id.items():
    out.write('%d\t%s\t%d\n' % (d, w, word_count[d]))

def map_id_line(line):
  lst = []
  for w in line:
    lst.append(word_id.setdefault(w, len(word_id) + 1))
  return lst

def count_df(f, have_num=False, mapid=False):
  seg = f + '.seg'
  id = f + '.id'
  id_text = ''
  for line in open(seg):
    line = line.strip().split()
    if not line:
      continue
    if mapid:
      line = map_id_line(line)
      id_text += ' '.join(str(x) for x in line) + '\n'
    for x in set(line):
      word_count[int(x)] += 1

  if mapid:
    open(id, 'w').write(id_text)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(USAGE)
    exit(1)

  input_list = open(sys.argv[1])

  mapid = True
  if os.path.exists(ID_WORD):
    init_word_id()
    mapid = False

  for f in input_list:
    f = f.strip()
    if not f or not os.path.exists(f):
      continue
    count_df(f, mapid=mapid)

  save_word_id()
  save_word_count()

