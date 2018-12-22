import heapq
import queue
n = 12
def toposort(graph, s, t):
    ind = [0 for i in range(n)]
    q = queue.Queue()
    for i, x in enumerate(graph):
        for j, y in enumerate(x):
            if y != -1:
                ind[j] = ind[j] + 1
    
    q.put(s)
    topo = []
    while not q.empty():
        x = q.get()
        topo.append(x)
        for j, y in enumerate(graph[x]):
            if y != -1:
                ind[j] = ind[j] - 1
                if ind[j] == 0:
                    q.put(j)
    return topo

def getTopLevel(graph, topo):
    top = [0 for i in range(n)]
    for i in topo:
        m = 0
        for j in range(len(topo)):
            if graph[j][i] != -1:
                if top[j] + graph[j][i]> m:
                    m = top[j] + graph[j][i]
        top[i] = m
    return top
        
def getBottomLevel(graph, topo):
    bottom = [0 for i in range(n)]
    for i in reversed(topo):
        m = 0
        for j in range(n):
            if graph[i][j] != -1:
                if bottom[j] + graph[i][j]> m:
                    m = bottom[j] + graph[i][j]
        bottom[i] = m
    return bottom

def haspath(graph, u, v):
    vis = set()
    q = queue.Queue()
    q.put(u)
    vis.add(u)
    while not q.empty():
        x = q.get()
        for j, p in enumerate(graph[x]):
            if p == -1 or j in vis:
                continue
            if j == v: return True
            q.put(j)
            vis.add(j)
    return False


def minLevel(graph, S, T, s, t):
    topo = toposort(graph, s, t)
    top = getTopLevel(graph, topo)
    bottom = getBottomLevel(graph, topo)
    h = []
    heapq.heapify(h)
    for i in S:
        for j in T:
            heapq.heappush(h, [top[j] + bottom[i], i, j])
    
    cand = heapq.heappop(h)
    while (len(h) != 0) and haspath(graph, cand[1], cand[2]):
        cand = heapq.heappop(h)
    if len(h) == 0:
        return 0, 0
    return cand[2], cand[1]