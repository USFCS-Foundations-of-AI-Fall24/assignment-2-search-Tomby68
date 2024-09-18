from queue import PriorityQueue
from Graph import Node, Edge, Graph
from math import sqrt


class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "State: (%s) f: (%d)" % (self.location, self.f)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'

def goal_test(state):
    return state.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)
    total_states = 1
    mars_graph = start_state.mars_graph
    
    while search_queue:
        next_state = search_queue.get()
        if goal_test(next_state):
            break
        closed_list[next_state.location] = next_state
        edge_list = mars_graph.get_edges(Node(next_state.location))
        # Make new states from the adjacent edges, and add them
        # to the search_queue
        for edge in edge_list:
            if edge.dest not in closed_list:
                new_state = map_state(location=edge.dest, mars_graph=mars_graph, 
                prev_state=next_state, g=next_state.g+1, h=heuristic_fn(edge.dest))
                search_queue.put(new_state)
                total_states += 1
    print("Total states generated:", total_states)
#    print("all states generated: ")
#    for location, state in closed_list.items():
#        print(state)


## default heuristic - we can use this to implement uniform cost search
def h1(location) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(location) :
    location = location.split(",")
    x2 = int(location[0])
    y2 = int(location[1])
    return sqrt((x2 - 1)**2 + (y2 - 1)**2)

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    mars_graph = Graph(0)
    try:
        with open(filename) as graph_file:
            contents = graph_file.read()
        for line in contents.split("\n"):
            line = line.split(": ")       # line: [src, "destinations"]
            if len(line) > 1:                # Make sure it's not empty
                src_node = Node(line[0])
                mars_graph.add_node(src_node)
                destinations = line[1].split(" ")
                for dest_node in destinations:
                    mars_graph.add_node(Node(dest_node))
                    mars_graph.add_edge(Edge(src_node, dest_node))
    except FileNotFoundError as e:
        print(f"Unable to find file: {filename}")
    except Exception as e:
        print(e)
    return mars_graph


if __name__ == "__main__":
    mars_graph = read_mars_graph("MarsMap")
    start_state = map_state(location="8,8", mars_graph=mars_graph, g=0, h=sld("8,8"))
    #print(start_state)
    a_star(start_state, sld, goal_test)
    start_state = map_state(location="8,8", mars_graph=mars_graph, g=0, h=h1("8,8"))
    a_star(start_state, h1, goal_test)
        
