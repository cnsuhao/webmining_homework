#include "iostream"
#include "cassert"
#include "string"
#include "sstream"
#include "fstream"
#include "algorithm"
#include "cmath"
#include "vector"

using namespace std;

double kl_divergence(vector<double> P, vector<double> Q) {
  double sum = 0;
  assert(P.size() == Q.size());
  for (auto p = P.begin(), q = Q.begin(); p != P.end(); p++, q++) {
    sum += *p * log(*p / *q);
  }
  return sum;
}

void read(const char *file, vector<vector<double> > &vd) {
  ifstream fin;
  fin.open(file);  //ifstream::in
  for (string line; getline(fin, line); ) {
    vector<double> vt;
    double d;
    for (stringstream ss(line); ss >> d; ) {
      vt.push_back(d);
    }
    vd.push_back(vt);
  }
 }

int main(int argc, const char* argv[]) {
  
  if (argc != 3) {
    cerr << "Usage ./" << argv[0] << " file_a file_b" << endl;
  } 

  vector<vector<double> > A, B;
  read(argv[1], A);
  read(argv[2], B);

  double max_kl = -1, min_kl = -1;
  for (vector<double> a : A) {
    for (vector<double> b : B) {
      double kl = kl_divergence(a, b);
      if (min_kl == -1 || min_kl > kl) {
        min_kl = kl;
      }
      if (max_kl == -1 || max_kl < kl) {
        max_kl = kl;
      }
    }
  }
  cout << min_kl << endl << max_kl << endl;

  return 0;
}

