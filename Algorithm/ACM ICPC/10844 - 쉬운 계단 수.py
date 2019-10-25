n = int(input())
dp = [[0] + [1] * 9]
for i in range(1, n):
	step = []
	for j in range(0, 10):
		if j == 0 :
			step.append(dp[i-1][1])
		elif j > 0 and j < 9 :
			step.append(dp[i-1][j-1] + dp[i-1][j+1])
		elif j == 9:
			step.append(dp[i-1][8])
	dp.append(step)

sum = 0
for i in range(10):
	sum += dp[n-1][i]
print(sum % 1000000000)