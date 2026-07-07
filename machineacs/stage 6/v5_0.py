from collections import deque
import random 

#adjacency list
grph = {
    1: {2},
    2: {3,4},
    3: {},
    4: {5,6},
    5: {},
    6: {}
}

class Graph:
    
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes is not None else {}

    def add_node(self, id):
        self.nodes[id] = {}

    def add_edge(self, a,b):

        current_set = self.nodes[a]
        current_set.add(b)
        self.nodes[a] = current_set

        current_set = self.nodes[b]
        current_set.add(a)
        self.nodes[b] = current_set

    def neighbours(self, id):
        
        voisins = self.nodes[id]
        
        return voisins

def bfs_connected_components(grph):
    
    #build bfs algo

    graph = Graph(grph)
    
    q = deque()
    #q.append -> add to list 
    #q.popleft -> remove from list 

    visited = set()

    kys = grph.keys()

    output = {}

    for key in kys:

        if key not in visited:
            label = key
            q.append(key)

        while q:
        
            current_node = q.popleft()

            visited.add(current_node)
                
            output[current_node] = label
        
            voisins = graph.neighbours(current_node)

            for neighbour in voisins:
                if neighbour not in visited:
                    q.append(neighbour)
                    
    return output   
        

# adjacency list
graph = {
    1: {2},
    2: {3, 4},
    3: set(),
    4: {5, 6},
    5: set(),
    6: set(),
}

parents = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}

rank = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
}


class UnionFind:

    def __init__(self,a,b,grph):
        self.a = a
        self.b = b
        self.grph = grph
    
    def find(self,a):
        #find root of a
        nodes = [a]
        node = a
        parent = parents[node]
        
        while node != parent:
            
            if node not in nodes: nodes.append(node)
            parent = parents[node]
            node = parent
            parent = parents[node]
        
        for noeud in nodes:
            if parents[noeud] != parent:parents[noeud] = parent
        
        return parent 

    def union(self,a,b): 
         
        #find both of their roots
        a_root = self.find(a)
        b_root = self.find(b)

        if a_root == b_root:
            print("already united")
        
        else:

            a_rank = rank[a_root]
            b_rank = rank[b_root]

            if a_rank == b_rank:
                higher_root = a_root
                lower_root = b_root
                rank[higher_root] += 1
            else:
                higher_root = max(a_root, b_root, key=lambda root: rank[root])
                lower_root = min(a_root, b_root, key=lambda root: rank[root])

            parents[lower_root] = higher_root

        

    def components(self):
        compnents = {}
        for node in parents:
            root = self.find(node)
            if compnents[root]:
                compnents[root].append(node)
            else:
                compnents[root] = node
        
        return compnents


def main(a,b,grph):
    instance = UnionFind(a,b)
    instance.components()
    instance.find(a)
    bfs_connected_components(grph)

if __name__ == "__main__":
    # create a, b, and grph here
    a = 1
    b = 2

    grph = {
        1: [2],
        2: [1],
    }
    
    main(a, b, grph)