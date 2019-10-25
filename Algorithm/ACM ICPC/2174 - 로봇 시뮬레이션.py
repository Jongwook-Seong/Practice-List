A, B = map(int, input().split())
N, M = map(int, input().split())
C = [[0] * (A+2) for i in range(B+2)]
R = [0]
for i in range(1, N+1):
	R.append(input().split())
	R[i][0], R[i][1] = int(R[i][0]), int(R[i][1])
	C[R[i][0]][R[i][1]] = i

def isWallCrash(Rn):
	if R[Rn][2] == 'N':
		if R[Rn][1] < B:
			return False
		else:
			return True
	elif R[Rn][2] == 'W':
		if R[Rn][0] > 1:
			return False
		else:
			return True
	elif R[Rn][2] == 'E':
		if R[Rn][0] < A:
			return False
		else:
			return True
	elif R[Rn][2] == 'S':
		if R[Rn][1] > 1:
			return False
		else:
			return True
	else:
		print("isWallCrash error")

def checkRobotCrash(Rn):
	if R[Rn][2] == 'N':
		if C[R[Rn][0]][R[Rn][1] + 1] == 0:
			return False, 0
		else:
			return True, C[R[Rn][0]][R[Rn][1] + 1]
	elif R[Rn][2] == 'W':
		if C[R[Rn][0] - 1][R[Rn][1]] == 0:
			return False, 0
		else:
			return True, C[R[Rn][0] - 1][R[Rn][1]]
	elif R[Rn][2] == 'E':
		if C[R[Rn][0] + 1][R[Rn][1]] == 0:
			return False, 0
		else:
			return True, C[R[Rn][0] + 1][R[Rn][1]]
	elif R[Rn][2] == 'S':
		if C[R[Rn][0]][R[Rn][1] - 1] == 0:
			return False, 0
		else:
			return True, C[R[Rn][0]][R[Rn][1] - 1]
	else:
		print("isRobotCrash error")
		return False, -1

def goFront(Rn, direction):
	if direction == 'N':
		C[R[Rn][0]][R[Rn][1] + 1] = Rn
		C[R[Rn][0]][R[Rn][1]] = 0
		R[Rn][1] += 1
	elif direction == 'W':
		C[R[Rn][0] - 1][R[Rn][1]] = Rn
		C[R[Rn][0]][R[Rn][1]] = 0
		R[Rn][0] -= 1
	elif direction == 'E':
		C[R[Rn][0] + 1][R[Rn][1]] = Rn
		C[R[Rn][0]][R[Rn][1]] = 0
		R[Rn][0] += 1
	elif direction == 'S':
		C[R[Rn][0]][R[Rn][1] - 1] = Rn
		C[R[Rn][0]][R[Rn][1]] = 0
		R[Rn][1] -= 1
	else:
		print("goFront error")

def turnDirection(Rn, direction):
	if direction == 'L':
		if R[Rn][2] == 'N':
			R[Rn][2] = 'W'
		elif R[Rn][2] == 'W':
			R[Rn][2] = 'S'
		elif R[Rn][2] == 'S':
			R[Rn][2] = 'E'
		elif R[Rn][2] == 'E':
			R[Rn][2] = 'N'
	elif direction == 'R':
		if R[Rn][2] == 'N':
			R[Rn][2] = 'E'
		elif R[Rn][2] == 'E':
			R[Rn][2] = 'S'
		elif R[Rn][2] == 'S':
			R[Rn][2] = 'W'
		elif R[Rn][2] == 'W':
			R[Rn][2] = 'N'
	else:
		print("turnDirection error")

def simulate(inst):
	for i in range(inst[2]):
		if inst[1] == 'F':
			if isWallCrash(inst[0]):
				print("Robot " + str(inst[0]) + " crashes into the wall")
				return
			isRobotCrash, crashedRobotNum = checkRobotCrash(inst[0])
			if isRobotCrash:
				print("Robot " + str(inst[0]) + " crashes into robot " + str(crashedRobotNum))
				return
			goFront(inst[0], R[inst[0]][2])
		else:
			turnDirection(inst[0], inst[1])
	print("OK")
	return

for i in range(M):
	inst = input().split()
	inst[0], inst[2] = int(inst[0]), int(inst[2])
	simulate(inst)