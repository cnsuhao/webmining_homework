#!/user/bin/python3

USAGE = \
'''
python3 filter_id.py input_list want_df
want_id is comma seperated expression:
    a-b,c-d,e,f
'''

import sys, os
import bisect

ID_WORD = 'id_word.txt.sort'
ID_WORD_COUNT = 'id_word_count.txt.sort'
NEW_ID_WORD = 'new_id_word.txt'

def init_id_word():
  id_word = ['']
  for line in open(ID_WORD):
    line = line.strip().split('\t')
    id_word.append(line[1])
  return id_word

# change id to new id, start from 1
# if id not in want_id
#   return n+1 if id < l        LOW
#   return n+2 if l < id < h    MID
#   return n+3 if h < id        HIGH
def get_new_id(id, want_id):
  n = len(want_id)
  ix = bisect.bisect_left(want_id, id)
  if ix < n and want_id[ix] == id:
    return ix + 1
  else:
    if id < want_id[0]: return n + 1
    return n + 2 if id < want_id[n-1] else n+3

def get_want_id(want_df):
  want_df = want_df.split(',')
  want_df_lst = []
  for x in want_df:
    x = x.split('-')
    if len(x) == 2:
      a = int(x[0])
      b = int(x[1])
      assert a <= b
      want_df_lst += range(a, b+1)
    elif len(x) == 1:
      want_df_lst += [int(x[0])]
    else:
      print('Can\'t recognize %s' % ('-'.join(x)))
  want_df = set(want_df_lst)

  want_id = []
  for line in open(ID_WORD_COUNT):
    id, w, df, uf = line.strip().split()  # why \t doesn't work?
    if id == 'wid':  # header line
      continue
    id = int(id)
    df = int(df)
    if df in want_df:
      want_id.append(id)

  return sorted(want_id)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print(USAGE)
    exit(1)

  input_list = sys.argv[1]
  want_id = get_want_id(sys.argv[2])
  id_word = init_id_word()

  for f in open(input_list):
    f = f.strip()
    if not os.path.exists(f):
      continue
    out = open(f + '.nid', 'w')
    for line in open(f):
      nid = [get_new_id(int(id), want_id) \
             for id in line.strip().split()]
      out.write(' '.join(str(id) for id in nid) + '\n')
    out.close()

  # write new_id_word
  out = open(NEW_ID_WORD, 'w')
  for id in want_id:
    out.write('%d\t%s\n' % (get_new_id(id, want_id), id_word[id]))
  n = len(want_id)
  out.write('%d\tLOW\n' % (n+1))
  out.write('%d\tMID\n' % (n+2))
  out.write('%d\tHIGH\n' % (n+3))
  out.close()


