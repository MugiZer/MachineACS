from collections import deque

def binary_search(arr,target):

    len_arr = len(arr)
    left = 0
    right = len_arr - 1
    middle = (right + left) // 2
        
    value = arr[middle]

    while left <= right:

        if value > target:
            right = middle - 1
            new_middle = (left + right) // 2
            value = arr[new_middle]
            middle = new_middle 
        
        elif value < target:
            left = middle + 1
            new_middle = (left + right) // 2
            value = arr[new_middle]
            middle = new_middle 

        elif value == target:
            return middle 

    return(int(-1)) 


class HashTable:
    def __init__(self, capacity):
        # self lets you attach variables to this specific instance of the class
        self.capacity = capacity
        self.slots = [None] * self.capacity
        # The spec says: "No Python dict used internally — use a fixed-size list of slots."
       
    def insert(self, key, value):
        
        if type(key) == str:
            sum = 0
            
            for char in key:
                char_value = ord(char)
                sum += char_value 
            index = sum % self.capacity
        
        elif type(key) == int:
            index = key % self.capacity

        #collision handling
        condition = False 
        new_index = 0
        if self.slots[index]:

                while not condition and new_index <= self.capacity:
                    new_index = (index + 1) % self.capacity 
                    
                    if self.slots[new_index]:
                        index = new_index
                    
                    if not self.slots[new_index] or self.slots[new_index] == None or self.slots[new_index] == ("CERN", None):
                        self.slots[new_index] = (key,value)
                        condition = True 
            
        else:
            self.slots[index] = (key,value)
          
    def get(self, key):
        
        if type(key) == str:
            sum = 0
            
            for char in key:
                char_value = ord(char)
                sum += char_value 
            index = sum % self.capacity
        
        elif type(key) == int:
            index = key % self.capacity
        
        if self.slots[index] is None:
            return None 
        
        slot_key, slot_value = self.slots[index]
        
        if slot_key == key:
            return slot_value
        
        elif slot_key != key:
        
            #collision handling
            condition = False 
            original_index = index
            new_index = index + 1
        
            while not condition and new_index != original_index:
                new_index = (index + 1) % self.capacity 
                    
                if self.slots[new_index]:
                    slot_key,slot_value = self.slots[new_index]
                    
                    if slot_key != key:
                        index = new_index 

                    elif slot_key == key:
                        return slot_value
                
                elif self.slots[new_index] is None:
                    return None 


    def delete(self, key):
        
        if type(key) == str:
            sum = 0
        
            for char in key:
                char_value = ord(char)
                sum += char_value 
            index = sum % self.capacity
        
        elif type(key) == int:
            index = key % self.capacity
        
        if self.slots[index] is None:
            return None
        
        slot_key, slot_value = self.slots[index]
        
        if slot_key == key:
            self.slots[index] = ("CERN", None)
        
        elif slot_key != key:
        
            #collision handling
            condition = False 
            original_index = index
            new_index = index + 1
        
            while not condition and new_index != original_index:
                new_index = (index + 1) % self.capacity 
                    
                if self.slots[new_index]:
                    slot_key,slot_value = self.slots[new_index]
                    
                    if slot_key != key:
                        index = new_index 

                    elif slot_key == key:
                        self.slots[new_index] = ("CERN", None)
                
                elif self.slots[new_index] is None:
                    return None

def bfs(graph,start):
    #set up the queue 
    queue = deque()
    bfs_output = []
    visited = set()

    queue.append(start)
    visited.add(start)

    #establish BFS order and build up queue
    while len(queue) > 0:
        #get the current node
        current_node = queue.popleft()

        bfs_output.append(current_node)

        #get the neighbors 
        neighbors = graph[current_node]

        for neighbor in neighbors:
        
            if neighbor not in visited:
                queue.append(neighbor) 
                visited.add(neighbor)

    return bfs_output

def dfs(graph,start):
    queue = deque()
    dfs_output = []
    visited = set()

    queue.append(start)
    visited.add(start)

    while len(queue) > 0:
        
        current_node = queue.pop()
        
        if current_node not in dfs_output:
            dfs_output.append(current_node)

        neighbors = graph[current_node]

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return dfs_output


def topological_sort(graph):
    
    queue = deque()
    ts_output = []
    nodes = {}

    #calculate in-lines of nodes first
    for node in graph:
        nodes[node] = 0
    
    for node in graph:
        for node_ in graph[node]:
            nodes[node_] += 1

    for node in nodes:
        if nodes[node] == 0:
            queue.append(node)

        #as long as there are nodes to process
    while len(queue) > 0:

        #where the modifying in values happens

        current_node = queue.popleft()
        ts_output.append(current_node)

        child_nodes = graph[current_node]

        for child_node in child_nodes:
            nodes[child_node] -= 1
            if nodes[child_node] == 0:
                queue.append(child_node)

    if len(ts_output) < len(graph):
        raise ValueError("the DAG has a cycle")

    else:
        return ts_output