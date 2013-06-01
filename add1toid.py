
import os, sys

USAGE = \
'''
python3 add1toid.py input_list [have_num]
add 1 to id of file in input_list
have_num means at the begining of each line of the file, there is a word_num
Of course, this won't add 1
'''

def add1tofile(f, have_num=True):
 lines = open(f).readlines()
 with open(f, 'w') as out:
   for line in lines:
     line = line.strip().split()
     if not line:
       out.write('\n')
     else:
       line = [x if have_num and ix == 0 else str(int(x) + 1) \
               for (ix, x) in enumerate(line)]
       out.write(' '.join(line) + '\n')

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print(USAGE)
    exit(1)

  input_list = sys.argv[1]
  have_num = True if len(sys.argv) > 2 else False
  for f in open(input_list):
    f = f.strip()
    add1tofile(f, have_num)


