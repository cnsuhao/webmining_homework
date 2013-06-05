import sys, os, re
import numpy
from collections import defaultdict
import matplotlib.pyplot as plt
from operator import *
from math import log

USAGE = \
'''python3 top_var_features.py var|ent input_list theta k uid_depress out
For each user, find top k theta_d with high var
or least entropy?
'''

def sort_func(y, cmd):
  if cmd == 'var':
    return numpy.var(y)
  elif cmd == 'ent':
    # return sum(p*log(p))
    # -entropy(y)
    return sum(map(mul, y, map(log, y)))
  else:
    print('Can\'t recognize ' + cmd)
    exit(1)

if __name__ == '__main__':
  if len(sys.argv) != 7:
    print(USAGE)
    exit(1)

  input_list = [line.strip() for line in open(sys.argv[2])]
  theta = [[float(x) for x in line.split()] \
          for (ix, line ) in enumerate(open(sys.argv[3])) if ix > 0]
  assert len(input_list) == len(theta)

  k = int(sys.argv[4])
  depress_file = sys.argv[5]
  out = sys.argv[6]

  beg = defaultdict(lambda : len(input_list))
  end = defaultdict(int)
  for ix, line in enumerate(input_list):
    id = int(re.search('\w+/(\d+)', line).group(1))
    beg[id] = min(beg[id], ix)
    end[id] = max(end[id], ix)

  # is_plot = False
  out = open(out, 'w')
  uid_depress = [line.split() for line in open(depress_file)]
  for (ix, line) in enumerate(uid_depress):
    uid_depress[ix][1] = float(line[1])
    id = int(uid_depress[ix][0])
    nyy = numpy.array(theta[beg[id]:end[id]+1])
    nyy = sorted(nyy, key=lambda y: sort_func(y, sys.argv[1]), reverse=True)
    if len(nyy) < k:
      nyy = map(list, nyy) + [[1.0/100]*100] * (k-len(nyy))
    assert len(nyy) >= k
    out.write(str(uid_depress[ix][1]))
    for i in range(k):
      out.write('\t')
      out.write('\t'.join(map(str, nyy[i])))
      '''
      if not is_plot:
        plt.plot(range(len(nyy[i])), nyy[i])
        is_plot = True
      '''
    out.write('\n')
  out.close()
  '''
  plt.show()
  plt.savefig('xx.png')
  '''
