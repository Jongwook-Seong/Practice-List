/* acm icpc 1149 RGB°Å¸® */
#include <iostream>
#define MIN(a, b) (a < b ? a : b)
using namespace std;

int N;
int C[1001][3];
int T[1001][3];
int M;

void D() {
	for (int i = 0; i < 3; i++)
		T[0][i] = C[0][i];
	if (N == 2) {
		int min;
		min = MIN(T[1][0], T[1][1]);
		min = MIN(min, T[1][2]);
	}
	else {
		for (int i = 1; i < N; i++) {
			T[i][0] = C[i][0] + MIN(T[i - 1][1], T[i - 1][2]);
			T[i][1] = C[i][1] + MIN(T[i - 1][0], T[i - 1][2]);
			T[i][2] = C[i][2] + MIN(T[i - 1][0], T[i - 1][1]);
		}
	}
	M = MIN(T[N - 1][0], T[N - 1][1]);
	M = MIN(M, T[N - 1][2]);
}

int main() {
	cin >> N;
	for (int i = 0; i < N; i++)
		cin >> C[i][0] >> C[i][1] >> C[i][2];
	D();
	cout << M << endl;
	return 0;
}