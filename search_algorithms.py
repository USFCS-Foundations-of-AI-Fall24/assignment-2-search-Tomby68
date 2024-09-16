from collections import deque



## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    search_queue = deque()
    closed_list = {}

    search_queue.append((startState,""))
    total_states = 1
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            return next_state, total_states
        else :
            successors = next_state[0].successors(action_list)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            total_states += len(successors)
            search_queue.extend(successors)

    return None, None

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True,limit=0) :
    search_queue = deque()
    closed_list = {}

    search_queue.append((startState,""))
    total_states = 1
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.pop()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            return next_state, total_states
        else :
            successors = next_state[0].successors(action_list, limit)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            total_states += len(successors)
            search_queue.extend(successors)
    return None, None

## add iterative deepening search here
def iterative_deepening_search(startState, action_list, goal_test, use_closed_list=True, maxLimit=0) :
    result = None
    total_states = 0
    for i in range(1, maxLimit + 1):
        if result == None:
            result, states = depth_first_search(startState, action_list, goal_test, use_closed_list, maxLimit)
            total_states += states
    
