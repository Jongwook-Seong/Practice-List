n = int(input())
sum = 0
for i in range(1, n+1):
	for j in range(i+1):
		sum += i + j
print(sum)