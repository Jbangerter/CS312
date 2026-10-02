import sys

VERTEX = str
GRAPH = dict[VERTEX, list[VERTEX]]
COMPONENT = dict[VERTEX, list[int]]
PREPOSTNUMS = list[COMPONENT]
sys.setrecursionlimit(10000)


def prepost(graph: GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    index: int = 1
    visited: set[VERTEX]= set()
    prepost: PREPOSTNUMS = []

    for vertex in graph:
        if vertex not in visited:
            current_component: COMPONENT = {}
            prepost.append(current_component)
            index = DFS(vertex,graph,current_component,visited,index)

    return prepost


def DFS(vertex: VERTEX, graph:GRAPH, currentComponent:COMPONENT, visited: set[VERTEX], index) -> int:
        visited.add(vertex)
        currentComponent[vertex] = [index, -1]
        index = index + 1

        for neighbor in graph.get(vertex,[]):
            if neighbor not in visited:
                index = DFS(neighbor, graph, currentComponent, visited, index)

        currentComponent[vertex][1] = index
        index = index + 1

        return index

def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """

    prepostNumbers: PREPOSTNUMS = prepost(graph)
    postEntries: list[tuple[int,VERTEX]] = []

    for tree in prepostNumbers:
        for vertex,number in tree.items():
            postNum = number[1]
            postEntries.append((postNum,vertex))

    postEntries.sort(reverse=True)
    finishOrder = [vertex for postNum,vertex in postEntries]

    reversedGraph: GRAPH = reverse_graph(graph)

    visited: set[VERTEX] = set()
    sccs: list[set[VERTEX]] = []

    for vertex in finishOrder:
        if vertex not in visited:
            currentScc: set[VERTEX] = set()

            collect_scc(vertex,reversedGraph,visited,currentScc)
            sccs.append(currentScc)

    sccs.reverse()
    return sccs


def reverse_graph(graph: GRAPH) -> GRAPH:
    reversed_graph: GRAPH = {
        vertex: []
        for vertex in graph
    }

    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph[neighbor].append(vertex)

    return reversed_graph

def collect_scc(vertex: VERTEX,graph: GRAPH,visited: set[VERTEX],current_scc: set[VERTEX]) -> None:

    visited.add(vertex)
    current_scc.add(vertex)

    for neighbor in graph.get(vertex, []):
        if neighbor not in visited:
            collect_scc(neighbor,graph,visited,current_scc)



def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    indexes = {}

    for tree in trees:
        for vertex, numbers in tree.items():
            indexes[vertex] = numbers

    for source, neighbors in graph.items():
        for neighbor in neighbors:
            sourcePre, sourcePost = indexes[source]
            neighborPre, neighborPost = indexes[neighbor]

            if (sourcePre < neighborPre and neighborPost < sourcePost):
                classification['tree/forward'].add((source, neighbor))

            elif (neighborPre < sourcePre and sourcePost < neighborPost):
                classification['back'].add((source, neighbor))

            else:
                classification['cross'].add((source, neighbor))


    return classification


