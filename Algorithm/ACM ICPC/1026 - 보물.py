n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
result = 0
while a:
	result += a.pop(a.index(min(a))) * b.pop(b.index(max(b)))
print(result)