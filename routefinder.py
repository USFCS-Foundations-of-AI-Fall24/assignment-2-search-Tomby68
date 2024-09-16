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
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)

    while len(search_queue) > 0:

        # Process: 
'''
1. Dequeue a state
2. Add the state.loc to closed_list (we've now visited that location)
3. Check the map graph to find the adjacent nodes
4. For each adjacent node:
    Check if the location is in closed_list. If it is, skip it
    If it isn't, add it to the search_queue as a new state with the correct values
'''

## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    location = state.location.split(",")
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
    #mars_graph = read_mars_graph("MarsMap")
    #print(mars_graph.g)
        
