s = input()
for i in range(len(s) // 2 + 1):
	if s[i] != s[len(s)-i-1]:
		print(0)
		break
	elif i == len(s) // 2:
		print(1)