## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy
from search_algorithms import breadth_first_search
from search_algorithms import depth_first_search
from search_algorithms import iterative_deepening_search
from search_algorithms import subproblem_search

class RoverState :
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, charged=False, holding_tool=False):
        self.loc = loc
        self.sample_extracted=sample_extracted
        self.holding_sample = holding_sample
        self.charged=charged
        self.holding_tool = holding_tool
        self.prev = None

    ## you do this.
    def __eq__(self, other):
       return (self.loc == other.loc) and (
       self.sample_extracted == other.sample_extracted) and (
       self.holding_sample == other.holding_sample) and (
       self.charged == other.charged) and (
       self.holding_tool == other.holding_tool)
       
    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n"+
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Charged? {self.charged}\n" +
                f"Holding tool? {self.holding_tool}")

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions, limit=0, states_generated=0):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        succ = [(item(self), item.__name__) for item in list_of_actions]
        ## remove actions that have no effect

        succ = [item for item in succ if not item[0] == self]
        if limit > 0 and (len(succ) + states_generated) > limit :
            return succ[:limit - states_generated]
        return succ

# Say:
# states_generated = 5
# limit = 7
# len(succ = 3)
# Want to add just 2, so return succ[:2]
# return succ[:limit - states_generated]

## our actions will be functions that return a new state.

def move_to_sample(state) :
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev=state
    return r2
def move_to_station(state) :
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2
def move_to_battery(state) :
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2
# add tool functions here

def pick_up_tool(state) :
    r2 = deepcopy(state)
    r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state) :
    r2 = deepcopy(state)
    r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state) :
    r2 = deepcopy(state)
    if state.holding_tool and state.loc == "sample":
        r2.sample_extracted = True
    r2.prev = state
    return r2

def pick_up_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample":
        r2.holding_sample = True
    r2.prev = state
    return r2

def drop_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "station":
        r2.holding_sample = False
    r2.prev = state
    return r2

def charge(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample":
        r2.charged = True
    r2.prev = state
    return r2


action_list = [charge, drop_sample, pick_up_sample,
               move_to_sample, move_to_battery, move_to_station,
               pick_up_tool, drop_tool, use_tool]

def returnToCharger(state) :
    return state.loc == "battery" and state.charged == True
## add your goals here.

def moveToSample(state):
    return state.loc == "sample"

def removeSample(state):
    return state.sample_extracted == True

#def holding_goal(state) : 
#    return state.holding_sample == False

def mission_complete(state) :
    return returnToCharger(state) and removeSample(state)

def main():
    limit = 20
    s = RoverState()
    #s = RoverState()
    bfs_result, bfs_states = breadth_first_search(s, action_list, mission_complete)
    dfs, dfs_states = depth_first_search(s, action_list, mission_complete)
    dfs_result, dfs_lim_states = depth_first_search(s, action_list, mission_complete, limit=limit)
    #print("BFS result:", bfs_result)
    #print("DFS result:", dfs_result)
    ids_result, ids_states = iterative_deepening_search(s, action_list, mission_complete, maxLimit=limit)
    #print("IDS result:", ids_result)
    decomp_result, decomp_states = subproblem_search(breadth_first_search, [moveToSample, removeSample, returnToCharger], s, action_list)
    print(f"BFS states: {bfs_states}")
    print(f"DFS states: {dfs_states}")
    print(f"DFS with limit={limit} states: {dfs_lim_states}")
    print(f"IDS with maxLimit={limit} states: {ids_states}")
    print(f"Decomposition states (with BFS): {decomp_states}")

if __name__=="__main__" :
    main()
