import sys
from collections import deque

input = sys.stdin.readline
INF = 10 ** 10

N, K = map(int, input().split())

max_length = 1 + N * 3 + 1 # source -> nodes -> sink
graph = [[] for _ in range(max_length)]

def add_edge(start, end, capacity, cost):
    graph[start].append([end, len(graph[end]), 0, capacity, cost])
    graph[end].append([start, len(graph[start]) - 1, 0, 0, -cost])

add_edge(0, 1, K, 0) # source -> node(first)

for i in range(1, max_length - 1): # node -> next_node
    add_edge(i, i + 1, INF, 0)

for i, x in enumerate(list(map(int, input().split())), start = 1): # node jump
    jump = i + N

    if jump >= max_length:
        add_edge(i, max_length - 1, 1, -x)
    
    else:
        add_edge(i, jump, 1, -x)

def spfa():
    q = deque()
    q.append(start_node)

    dist = [float('inf')] * max_length
    dist[start_node] = 0

    in_queue = [False] * max_length
    in_queue[start_node] = True

    while q:
        node = q.popleft()
        in_queue[node] = False

        for next_node, rev, flow, capacity, cost in graph[node]:
            if capacity > flow and dist[next_node] > cost + dist[node]:
                dist[next_node] = cost + dist[node]

                if not in_queue[next_node]:
                    in_queue[next_node] = True
                    q.append(next_node)

    return dist

def update():
    result = INF

    for node in range(max_length):
        if not visited[node]:
            continue

        for next_node, rev, flow, capacity, cost in graph[node]:
            if capacity > flow and not visited[next_node]:
                result = min(result, cost + dists[node] - dists[next_node])

    if result >= INF:
        return False

    for node in range(max_length):
        if not visited[node]:
            dists[node] += result

    return True

def flow_dfs(node, min_flow):
    visited[node] = True

    if node == end_node:
        return min_flow

    while work[node] < len(graph[node]):
        next_node, rev, flow, capacity, cost = graph[node][work[node]]

        if not visited[next_node] and capacity > flow and dists[next_node] == dists[node] + cost:
            available = capacity - flow
            result = flow_dfs(next_node, min(min_flow, available))

            if result > 0:
                graph[node][work[node]][2] += result
                graph[next_node][rev][2] -= result
                return result

        work[node] += 1

    return 0

start_node = 0
end_node = max_length - 1
total = 0

dists = spfa()

while True:
    work = [0] * max_length

    while True:
        visited = [False] * max_length 
        flow = flow_dfs(start_node, INF)

        if flow == 0:
            break

        total += dists[end_node]

    if not update():
        break

print(-total)