import argparse

def arguments():
    parser = argparse.ArgumentParser(description="Spell Checker CLI")
    parser.add_argument("text_file", help="Path to the text file to check")
    parser.add_argument("dict_file", help="Path to the dictionary file (one word per line)")
    parser.add_argument("--suggestions", type=int, default=5, help="Number of suggestions per misspelled word (default 5)")
    
    args = parser.parse_args()
    
    return args.text_file, args.dict_file, args.suggestions

text_path, dict_path, suggestions = arguments()

class HashTable:

    def __init__(self, size):
        self.size = size
        self.list = [None] * size 

    def insert(self, key, value):
        
        if type(key) == str:
            
            key_val = 0

            for char in key:
                key_val += ord(char)

            original_index = key_val % self.size

        elif type(key) == int:

            key_val = 0

            original_index = key_val % self.size
        
        if self.list[original_index] == None:
            self.list[original_index] = (key,value)

        else:
            
            condition = False
            
            max_index = len(self.list)

            index = original_index

            new_index = -1
            
            while not condition and new_index != original_index:

                new_index = index + 1
                
                if new_index == max_index:
                    new_index = 0
                
                if self.list[new_index] == None:

                    self.list[new_index] = (key,value)
                    condition = True 

                elif self.list[new_index] and self.list[new_index] != None:
                    index = new_index 

    def get(self, key):

        if type(key) == str:
            
            key_val = 0

            for char in key:
                key_val += ord(char)

            index = key_val % self.size

        elif type(key) == int:

            key_val = 0

            index = key_val % self.size

        lst = self.list

        if lst[index]:

            lst_key, value = lst[index]

            if lst_key == key:
                return (lst_key,value)

            elif lst_key != key:

                original_index = index
                max_index = len(lst)
                new_index = 0
                condition = False 

                while not condition and new_index != original_index:

                    new_index = index + 1

                    if new_index < max_index:
                        pass

                    elif new_index == max_index:
                        new_index = 0

                    if lst[new_index]:

                        lst_key, value = lst[new_index]

                        if lst_key == key:
                            condition = True 
                            return(lst_key,value)

                        else:
                            index = new_index 

                    else:
                        return(None)

        else:
            return(None)

#load every word in dict into hashtable 
def load_dict(path):

    with open(path) as f:

        dictionary = f.readlines()

        hash_table = HashTable(500000)

        for word in dictionary:
            word = word.lower().strip()
            word = word.strip(".,!?;:\"'()-")
            hash_table.insert(word, value=word)

        return hash_table,dictionary

def read_file(path,table):

    results = []
    
    with open(path) as f:

        for line_num, line in enumerate(f,start=1):
            
            words = line.split()

            for word in words:
                
                word = word.lower().strip()
                word = word.strip(".,!?;:\"'()-")
                check = table.get(word)

                if not check:
                    results.append((word,line_num))

    return results 


def levenshtein(mispelling,candidate):
    
    #initialize a grid 
    rows = len(mispelling) + 1
    cols = len(candidate) + 1 

    array = [[0]* cols for row in range(rows)]

    #initialize grid values

    #top row 
    for i in range(rows):
        array[i][0] = i

    #bottom row
    for j in range(cols):
        array[0][j] = j

    #matrix nested loop

    for i in range(1,rows):

        for j in range(1,cols):
        
            if mispelling[i-1] == candidate[j-1]:
                array[i][j] = array[i-1][j-1]

            else:

                delete = array[i-1][j]
                replace = array[i-1][j-1]
                insert = array[i][j-1]

                optimal_path = 1 + min(delete,replace,insert)
                array[i][j] = optimal_path

    edit_distance = array[-1][-1]

    return((edit_distance,candidate))

def compare(mispellings, dctionary):
    
    final_list = []

    for bad_word, line_num in mispellings:

        list_of_candidates = []

        for proper_word in dctionary:

            edit_distance,candidate = levenshtein(bad_word,proper_word)
            
            list_of_candidates.append((edit_distance,candidate,bad_word))

        list_of_candidates.sort()

        list_of_candidates = list_of_candidates[:5]

        final_list.append(list_of_candidates)

    return final_list


hsh_tbl,dict_ = load_dict(dict_path)
bad_words = read_file(text_path,hsh_tbl)
final_list = compare(bad_words,dict_)

del dict_

for candidates in final_list:

    suggestions = []
    
    for candidate in candidates:
            
        edit_distance,candidate,bad_word = candidate 

        suggestions.append( {bad_word : f"{edit_distance} : {candidate}"} )

    for suggestion in suggestions:
        print(suggestion)