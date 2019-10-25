/* acm icpc 1003 피보나치 함수 */
#include <iostream>
using namespace std;

int M[41] = { 1,1, };

int fibonacci(int n) {
	if (n <= 1) return M[n];
	else
		if (M[n] > 0) return M[n];
	return M[n] = fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
	int T; cin >> T;
	while (T--) {
		int N; cin >> N;
		if (N == 0) cout << "1 0" << endl;
		else if (N == 1) cout << "0 1" << endl;
		else {
			fibonacci(N);
			cout << M[N - 2] << ' ' << M[N - 1] << endl;
		}
	}
}