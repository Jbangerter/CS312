import math


class MinHeap:
    def __init__(self):
        self.heap = []
        self.pos = {}

    def swap(self, i, j):
        self.pos[self.heap[i][1]] = j
        self.pos[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def bubbleUp(self, i):
        parent = (i - 1) // 2
        while (i > 0 and self.heap[i][0] < self.heap[parent][0]):
            self.swap(i, parent)
            i = parent
            parent = (i - 1) // 2

    def bubbleDown(self, i):
        n = len(self.heap)
        while (True):
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if (left < n and self.heap[left][0] < self.heap[smallest][0]):
                smallest = left

            if (right < n and self.heap[right][0] < self.heap[smallest][0]):
                smallest = right

            if (smallest != i):
                self.swap(i, smallest)
                i = smallest
            else:
                break

    def extractMin(self):
        if (len(self.heap) == 0):
            return None, math.inf

        minDist, minNode = self.heap[0]
        self.pos.pop(minNode, None)

        last = self.heap.pop()
        if (len(self.heap) > 0):
            self.heap[0] = last
            self.pos[last[1]] = 0
            self.bubbleDown(0)

        return minNode, minDist

    def decreaseKey(self, node, newDist):
        i = self.pos[node]
        if (newDist < self.heap[i][0]):
            self.heap[i][0] = newDist
            self.bubbleUp(i)

    def contains(self, node):
        return (node in self.pos)

    def isEmpty(self):
        return (len(self.heap) == 0)

def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """


    distances = {}
    previousNodes = {}

    for node in graph.keys():
        distances[node] = math.inf
        previousNodes[node] = None

    distances[source] = 0.0

    pq = MinHeap()

    pq.heap.append([0.0, source])
    pq.pos[source] = 0

    idx = 1
    for node in graph.keys():
        if (node != source):
            pq.heap.append([math.inf, node])
            pq.pos[node] = idx
            idx += 1

    while (not pq.isEmpty()):
        currentNode, currentDist = pq.extractMin()

        if (currentDist == math.inf or currentNode == target):
            break

        for neighbor in graph[currentNode].keys():
            weight = graph[currentNode][neighbor]
            if (pq.contains(neighbor)):
                newDist = currentDist + weight

                if (newDist < distances[neighbor]):
                    distances[neighbor] = newDist
                    previousNodes[neighbor] = currentNode
                    pq.decreaseKey(neighbor, newDist)

    path = []
    current = target

    if (previousNodes[current] is not None or current == source):
        while (current is not None):
            path.insert(0, current)
            current = previousNodes[current]

    if (len(path) == 0 and source != target):
        return [], math.inf

    return path, distances[target]

def find_shortest_path_with_linear_pq(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """

    distances = {node: math.inf for node in graph.keys()}
    distances[source] = 0.0

    previousNodes = {node: None for node in graph.keys()}
    unvisited = list(graph.keys())

    while len(unvisited) > 0:
        currentNode = None
        minDist = math.inf
        for node in unvisited:
            if distances[node] < minDist:
                minDist = distances[node]
                currentNode = node

        if currentNode is None or currentNode == target:
            break

        unvisited.remove(currentNode)

        for neighbor, weight in graph[currentNode].items():
            if neighbor in unvisited:
                newDistance = distances[currentNode] + weight

                if newDistance < distances[neighbor]:
                    distances[neighbor] = newDistance
                    previousNodes[neighbor] = currentNode

    path = []
    current = target

    if previousNodes[current] is not None or current == source:
        while current is not None:
            path.insert(0, current)
            current = previousNodes[current]

    if not path and source != target:
        return [], float('inf')

    return path, distances[target]
