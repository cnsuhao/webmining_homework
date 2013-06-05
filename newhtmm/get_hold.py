
import sys, os

USAGE = \
'''python get_hold.py in_file k out_dir'''

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print(USAGE)
    exit(1)

  in_file = open(sys.argv[1])
  k = int(sys.argv[2])
  out_dir = sys.argv[3]
  if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

  for ix, line in enumerate(in_file):
    r = ix % k
    out = open(out_dir + '/' + str(r), 'a')
    out.write(line)
    out.close()
