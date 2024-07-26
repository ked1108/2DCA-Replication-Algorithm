import itertools
import math

class Cell:
    def __init__(self, value:str =None, i:int=None, j:int=None):
        self.value = value
        self.i = i
        self.j = j
        self.x = None
        self.y = None

    def set_pointers(self, cell1, cell2):
        self.x = cell1
        self.y = cell2

    def set_x(self, cell1):
        self.x = cell1

    def set_y(self, cell2):
        self.y = cell2
    
    def __repr__(self):
        pointer1_value = self.x.value if self.x else None
        pointer2_value = self.y.value if self.y else None
        return f"Cell {self.value}"
    
def get_pos(x, y, size):
    return x+y*size

def check_in_bounds(i, j, x, y):
    return i >= 0 and i < x and j >= 0 and j < y

def set_neighbourhood(rule_l):
    neighbours = [0]*9
    neighbours[0] = rule_l[6]
    neighbours[1] = rule_l[7]
    neighbours[2] = rule_l[8]
    neighbours[3] = rule_l[5]
    neighbours[4] = rule_l[0]
    neighbours[5] = rule_l[1]
    neighbours[6] = rule_l[4]
    neighbours[7] = rule_l[3]
    neighbours[8] = rule_l[2]
    return neighbours

def apply_rule(rule:int, x:int, y:int, image):
    rule_l = list(map(lambda x: int(x), list(format(rule, '09b'))))
    rule_l.reverse()
    neighbours = set_neighbourhood(rule_l)
    for i in range(y):
        for j in range(x):
            # print(image[get_pos(j, i, x)])
            cell = image[get_pos(j, i, x)]
            ct = 0
            for y_ in range(-1,2):
                for x_ in range(-1, 2):
                    if check_in_bounds(j+x_, i+y_, x, y) and neighbours[ct] == 1:
                        neighbour = image[get_pos(j+x_, i+y_, x)]
                        if cell.x is None:
                            cell.set_x(neighbour)
                        elif cell.y is None:
                            cell.set_y(neighbour)
                    ct+=1            


def create_adj_matrix(x:int, y:int, image):
    adj_matrix = [[0 for j in range(len(image))] for i in range(len(image))]
    for i, cell in enumerate(image):
        if cell.x is not None:
            adj_matrix[i][get_pos(cell.x.j-1, cell.x.i-1, x)] = 1
        if cell.y is not None:
            adj_matrix[i][get_pos(cell.y.j-1, cell.y.i-1, x)] = 1
    
    return adj_matrix


def find_incoming_nodes(pos:int, image, adj_matrix):
    nodes = []
    for i in range(len(image)):
        if adj_matrix[i][pos] == 1:
            nodes.append(image[i])
    
    return nodes

def find_outgoing_nodes(pos:int, image, adj_matrix):
    return [image[i] for i in range(len(image)) if adj_matrix[pos][i] == 1]


def find_chain(pos:int, x, y, chain:set, frm:Cell, image, adj_matrix):
    chain.add(image[pos])
    
    incoming = find_incoming_nodes(pos, image, adj_matrix)
    incoming = [node for node in incoming if node is not frm]
    for node in incoming:
        outgoing = find_outgoing_nodes(get_pos(node.j-1, node.i-1, x), image, adj_matrix)
        for n in outgoing:
            if n is not image[pos]:
                find_chain(get_pos(n.j-1, n.i-1, x), x, y, chain, node, image, adj_matrix)


def find_max(rule: int, x, y, image, adj_matrix, memory:dict):
    if(rule in memory.keys()):
        return memory[rule]
    
    maxx = 0
    longest_chain = set()
    for i in range(y):
        for j in range(x):
            chain = set()
            find_chain(get_pos(j, i, x), x, y, chain, None, image, adj_matrix)
            if len(chain) > maxx:
                longest_chain = chain
                maxx = len(chain)
    
    # print(longest_chain)
    memory[rule] = (maxx, longest_chain)
    return (maxx, longest_chain)


def conv_to_c2(rule: int):
    l = list(map(int, reversed(list(format(rule, '09b')))))
    l = [i for i,j in enumerate(l) if j != 0]
    comps = list(map(lambda x:2**x[0]+2**x[1], itertools.combinations(l, 2)))
    
    return comps
    

def find_k(rule: int, x:int, y:int, memory:dict):
    comps = conv_to_c2(rule)
    m = 0
    longest_chain = set()
    for r in comps:
        image = [Cell("B"+str(i)+str(j), i, j) for i in range(1,y+1) for j in range(1,x+1)]
        apply_rule(r, x, y, image)
        adj_matrix = create_adj_matrix(x, y, image)
        res = find_max(r, x, y, image, adj_matrix, memory)
        if res[0] > m:
            m = res[0]
            longest_chain = res[1]
    return (m, longest_chain)

if __name__ == "__main__":
    x = int(input("Enter the number of rows:\t"))
    y = int(input("Enter the number of columns:\t"))
    rule = int(input("Enter the rule:\t"))
    m, chain = find_k(rule, x, y, {})
    print("Longest Chain:\t", chain)
    print("Value of k:\t", 2**math.ceil(math.log2(m)))
    