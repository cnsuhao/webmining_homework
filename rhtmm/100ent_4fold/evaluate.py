
import sys, os
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from pylab import *
import numpy as np
from operator import *

USAGE = \
'''python evaluate.py in_dir k_fold top_k
cross validation using top_k var topic distribution in feature files
Make sure features in in_dir should have more than top_k topic distribution'''


def mean_absolute_error(x, y):
  return np.average(map(abs, map(sub, x, y)))

def main(in_dir, k_fold, top_k):
  assert type(k_fold) == int
  assert type(top_k) == int
  sum = 0
  for k in range(k_fold):
    test = [map(float, line.split()) for line in open(in_dir + '/' + str(k))]
    train = [map(float, line.split()) for kk in range(k_fold) if kk != k \
             for line in open(in_dir + '/' + str(kk))]

    train = sorted(train, key = lambda x : x[0], reverse = True)
    train, test = np.array(train), np.array(test)
    assert size(train, 1) >= 100 * top_k + 1
    X, Y = train[:, 1:100*top_k+1], train[:, 0]
    tX, tY = test[:, 1:100*top_k+1], test[:, 0]
    clf = GradientBoostingRegressor(n_estimators=10, learning_rate=0.1, \
            max_depth=1, random_state=0, loss='ls').fit(X, Y)
    #clf = SVR(C=0.5, kernel='linear', epsilon=1e-4, tol=1e-5)
    clf.fit(X, Y)
    '''
    print('train error: %f test error %f' % \
          (mean_absolute_error(clf.predict(X), Y), \
          mean_absolute_error(clf.predict(tX), tY)))
    '''
    sum += mean_absolute_error(clf.predict(tX), tY)
    #plot(clf.predict(X))
    #plot(Y)
  #show()
  return sum / k_fold

# predict every user with 0.5 depress value
def half_depress(in_dir, k_fold, top_k):
  assert type(k_fold) == int
  assert type(top_k) == int
  sum = 0
  for k in range(k_fold):
    test = [map(float, line.split()) for line in open(in_dir + '/' + str(k))]
    test = np.array(test)
    tX, tY = test[:, 1:100*top_k+1], test[:, 0]
    #m = (0.92354231 + 0.02981475) / 2
    m = 0.5
    sum += mean_absolute_error([m]*len(tY), tY)
  return sum / k_fold


if __name__ == '__main__':
  if len(sys.argv) != 4:
    print(USAGE)
    exit(1)

  in_dir = sys.argv[1]
  k_fold = int(sys.argv[2])
  top_k = int(sys.argv[3])

  print('%d fold cv, mean absolute error: %f' %
        (k_fold, main(in_dir, k_fold, top_k)))
