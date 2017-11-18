from model.graph import *

def constructVertexOrderDFS(graph):
    nodes = []
    stack = [graph.nodes[0]]

    while stack:
        cur_node = stack[0]

        stack = stack[1:]
        if cur_node.id not in nodes:
            nodes.append(cur_node.id)

        rev = cur_node.getNeighboursSorted()
        rev.reverse()
        for child in rev:
            if child.id not in nodes:
                stack.insert(0, child)

    for n in graph.nodes:
        if n.id not in nodes:
            nodes.append(n.id)

    graph.reorder(nodes)

    return nodes