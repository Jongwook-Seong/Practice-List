/* acm icpc 1149 RGB°Å¸® */
#include <iostream>
using namespace std;

int A[3003] = { 0, };

int F(int N, int C) {
	if (N > 0) {
		int C1 = F(N - 1, (C + 1) % 3);
		int C2 = F(N - 1, (C + 2) % 3);
		return A[3 * N + C] + (C1 < C2 ? C1 : C2);
	}
	else return A[(C + 1) % 3] < A[(C + 2) % 3] ? A[(C + 1) % 3] : A[(C + 2) % 3];
}

int main() {
	int N; cin >> N;
	for (int i = 0; i < N; i++)
		cin >> A[i*3] >> A[i*3 + 1] >> A[i*3 + 2];
	A[3 * N] = F(N - 1, 0);
	A[3 * N + 1] = F(N - 1, 1);
	A[3 * N + 2] = F(N - 1, 2);
	int min = (A[3 * N] < A[3 * N + 1] ? A[3 * N] : A[3 * N + 1]);
	min = (min < A[3 * N + 2] ? min : A[3 * N + 2]);
	cout << min;
	return 0;
}