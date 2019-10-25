n = int(input())

dp = []

dp.append(0)
dp.append(0)
dp.append(1)
dp.append(1)

for i in range(4, n + 1):
	dp.append(dp[i - 1] + 1);
	if(i % 2 == 0):
		dp[i] = min(dp[i], dp[i // 2] + 1)
	if(i % 3 == 0):
		dp[i] = min(dp[i], dp[i // 3] + 1)

print(dp[n])