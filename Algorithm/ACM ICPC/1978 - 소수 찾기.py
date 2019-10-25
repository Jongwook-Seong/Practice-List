import math
n = int(input())
numlist = list(map(int, input().split()))
numFilter = list(range(2, 1001))
count = 0
for i in range(2, math.ceil(math.sqrt(1000))):
	for j in numFilter:
		if j / i == 1: pass
		elif j % i == 0: numFilter.remove(j)
for i in numlist:
	if i in numFilter:
		count += 1
print(count)