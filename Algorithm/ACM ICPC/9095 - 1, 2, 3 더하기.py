tc = int(input())
a = [0, 1, 2, 4]
# total number of case of 1 + a[i-1], 2 + a[i-2], and 3 + a[i-3]
for i in range(4, 11):
	a.append(a[i-1] + a[i-2] + a[i-3])
for t in range(0, tc):
	n = int(input())
	print(a[n])