
import os, sys

USAGE = \
'''
python3 add_w_num.py input_list
'''

if __name__ == '__main__':

  if len(sys.argv) != 2:
    print(USAGE)
    exit(1)

  input_list = sys.argv[1]
  for f in open(input_list):
    f = f.strip()
    if not os.path.exists(f):
      continue
    lines = [line.strip().split() for line in open(f)]
    out = open(f, 'w')
    for line in lines:
      line.insert(0, str(len(line)))
      out.write(' '.join(line) + '\n')
    out.close()
