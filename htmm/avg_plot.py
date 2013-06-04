
import sys, os, re, numpy
from matplotlib import *
from pylab import *
from collections import defaultdict

USAGE = \
'''python avg_plot.py input_list theta uid_depress'''

def avg_plot(nyy):
  m = numpy.size(nyy, 1)
  yy = [0] * m
  for i in range(m):
    yy[i] = numpy.average(nyy[:, i])
  return yy

def max_var_plot(nyy):
  m = numpy.size(nyy, 1)
  yy = [0] * m
  for i in range(numpy.size(nyy, 0)):
    if numpy.var(yy) < numpy.var(nyy[i,:]):
      yy = nyy[i, :]
  return yy

def var_trend_plot(nyy, file_list):
  n = numpy.size(nyy, 0)
  assert n == len(file_list)
  pos_list = range(n)
  pos_list = sorted(pos_list, key=lambda x : (len(file_list[x]), file_list[x]))
  yy = [0] * n
  for (ix, p) in enumerate(pos_list):
    yy[ix] = numpy.var(nyy[p,:])
  return yy

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print(USAGE)
    exit(1)

  input_list = [line.strip() for line in open(sys.argv[1])]
  theta = [[float(x) for x in line.split()] \
          for (ix, line ) in enumerate(open(sys.argv[2])) if ix > 0]
  assert len(input_list) == len(theta)

  beg = defaultdict(lambda : len(input_list))
  end = defaultdict(int)
  for ix, line in enumerate(input_list):
    id = int(re.search('\w+/(\d+)', line).group(1))
    beg[id] = min(beg[id], ix)
    end[id] = max(end[id], ix)


  uid_depress = [line.split() for line in open(sys.argv[3])]
  n = len(uid_depress)

  plt.figure(figsize = (8, 6*n))

  for (ix, line) in enumerate(uid_depress):
    uid_depress[ix][1] = float(line[1])
    id = int(uid_depress[ix][0])
    # print(beg[id], end[id])

    nyy = numpy.array(theta[beg[id]:end[id]+1])
    m = numpy.size(nyy, 1)
    # yy = avg_plot(nyy)
    # yy = max_var_plot(nyy)
    yy = var_trend_plot(nyy, input_list[beg[id]:end[id]+1])
    ax = subplot(n, 1, ix+1)
    ax.plot(range(len(yy)), yy, label='%d    %f' % (id, uid_depress[ix][1]))
    ax.legend()

  plt.plot()
  #plt.savefig('all_max_var.png')
  #plt.savefig('all_var_trend.png')
  plt.savefig('kl.png')


