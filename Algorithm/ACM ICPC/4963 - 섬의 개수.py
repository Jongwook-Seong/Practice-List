import collections

def bfs(v):
	q = collections.deque()
	q.append(v)
	while q:
		v = q.popleft()
		for k in range(8):
			i = v[0] + di[k]
			j = v[1] + dj[k]
			if 0 <= i < h and 0 <= j < w and ocean[i][j]:
				ocean[i][j] = 0
				q.append([i, j])

di = [-1, -1, -1, 0, 0, 1, 1, 1]
dj = [-1, 0, 1, -1, 1, -1, 0, 1]

while True:
	w, h = map(int, input().split())
	if w == 0 and h == 0: break # end
	ocean = [list(map(int, input().split())) for i in range(h)]
	count = 0
	for i in range(h):
		for j in range(w):
			if ocean[i][j]: # Land
				count += 1
				bfs([i, j])
	print(count)