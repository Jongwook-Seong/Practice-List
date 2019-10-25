a = []
[a.append(list(list(map(int, input().split())))) for i in range(4)]
sum = [0] * 4
for i in range(4):
	if i == 0:
		sum[i] = a[i][1] - a[i][0]
	else:
		sum[i] = sum[i-1] + a[i][1] - a[i][0]
print(max(sum))