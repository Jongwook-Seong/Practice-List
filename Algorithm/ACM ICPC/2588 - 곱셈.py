num1, num2str = int(input()), input()
for i in range(len(num2str)-1, -1, -1):
	print(num1 * int(num2str[i]))
print(num1 * int(num2str))