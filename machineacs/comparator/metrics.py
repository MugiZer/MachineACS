def levenshtein_tabulated(s1, s2):

    #grid initializing 

    rows = len(s1) + 1
    cols = len(s2) + 1
    
    dp = [[0]*cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i 

    for j in range(cols):
        dp[0][j] = j 

    for i in range(1,rows):

        for j in range(1,cols):

            #if characters match -> do nothing, dp[i-1][j-1] is moving backwards diagonally in the matrix, which is just looking at the string without their current final characters, if characters match then no edit is needed so we just look at what the edit cost was before these characters
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] 
            
            else:
            
                insert = dp[i][j-1] + 1
                delete = dp[i-1][j] + 1
                replace = dp[i-1][j-1] + 1

                optimal_path = min(insert,delete,replace)
                dp[i][j] = optimal_path
    
    #backtracking
    i, j = len(s1), len(s2)
    operations = []
    
    #while we're not at the "" to ""
    while i > 0 and j > 0:
        
        #case 1 characters match
       
        #verifying wether [i][j] is result of replace edit
        if i > 0 and j > 0 and s1[i-1] == s2[j-1]:
            operations.append(f"no edits")
            i -= 1
            j -= 1

        #case 2 characters don't match 
        
        #insertion
        elif dp[i][j] == dp[i][j-1] + 1:
            operations.append(f"insert '{s2[j-1]}' ")
            j -= 1

        #delete
        elif dp[i][j] == dp[i-1][j] + 1:
            operations.append(f"delete '{s1[i-1]}'")
            i -= 1

        elif dp[i][j] == dp[i-1][j-1] + 1:
            operations.append(f"replace '{s1[i-1]}' with '{s2[j-1]}' ")
            i -= 1
            j -= 1
    
    while i > 0:
        operations.append(f"delete '{s1[i-1]}'")
        i -= 1

    while j > 0:
        operations.append(f"insert '{s2[j-1]}'")
        j -= 1

    return operations, dp, dp[rows-1][cols-1]


def jaccard_sim(s1,s2):
    
    s1_set = set(s1.split())
    s2_set = set(s2.split())

    union = (s1_set|s2_set) 

    intersection = (s1_set & s2_set)

    if not s1 and not s2:
        jaccard_similarity = 1.0 

    if len(union) != 0:
        jaccard_similarity = len(intersection) / len(union)

    return jaccard_similarity 


    
    

