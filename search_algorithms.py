from collections import deque

# subproblem_search assumes the end goal is mission_complete in mars_planner.py
def subproblem_search(search_algorithm, goal_tests_list, startState, action_list, use_closed_list=True, limit=0) :
    states_made = []
    next_start_state, total_states = search_algorithm(startState, action_list, goal_tests_list[0], use_closed_list)
    states_made.append(total_states)
    for goal_test in goal_tests_list[1:]:
        next_start_state, intermediate_states = search_algorithm(next_start_state[0], action_list, goal_test, use_closed_list)
        states_made.append(intermediate_states)
    #print(f"Total states generated by subproblem decomposition: {total_states}")
    return next_start_state, states_made
    

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
            #print("Goal found")
            #print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                #print(ptr)
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
            #print("Goal found")
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                #print(ptr)
            return next_state, total_states
        else :
            successors = next_state[0].successors(action_list, limit, total_states)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            total_states += len(successors)
            search_queue.extend(successors)

## add iterative deepening search here
def iterative_deepening_search(startState, action_list, goal_test, use_closed_list=True, maxLimit=0) :
    total_states = 0
    loop_states = 1
    for limit in range(1, maxLimit + 1):
        total_states += loop_states
        search_queue = deque()
        closed_list = {}
    
        search_queue.append((startState,""))
        loop_states = 1
        if use_closed_list :
            closed_list[startState] = True
            while len(search_queue) > 0 :
                ## this is a (state, "action") tuple
                next_state = search_queue.pop()
                if goal_test(next_state[0]):
                    #print("Goal found")
                    #print(next_state)
                    ptr = next_state[0]
                    while ptr is not None :
                        ptr = ptr.prev
                        #print(ptr)
                    total_states += loop_states
                    return next_state, total_states
                else :
                    successors = next_state[0].successors(action_list, limit, loop_states)
                    if use_closed_list :
                        successors = [item for item in successors
                                            if item[0] not in closed_list]
                        for s in successors :
                            closed_list[s[0]] = True
                    loop_states += len(successors)
                    search_queue.extend(successors)
