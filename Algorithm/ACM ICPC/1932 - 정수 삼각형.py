n = int(input())
num = []
for i in range(0, n):
	num.append(list(map(int, input().split())))

for i in range(n-1, 0, -1):
	if i == 0: break;
	for j in range(0, i):
		if num[i][j] > num[i][j+1]:
			num[i-1][j] = num[i-1][j] + num[i][j]
		else:
			num[i-1][j] = num[i-1][j] + num[i][j+1]

print(num[0][0])