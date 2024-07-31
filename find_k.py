import itertools
import math

def print_cell(pos: int, size:int):
    i = pos//size
    j = pos%size
    return f"Cell {j}{i}"

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

    n = []
    ct = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if neighbours[ct]:
                n.append((y, x))
            ct += 1

    return n

def apply_rule(rule:int, x:int, y:int, image):
    rule_l = list(map(lambda x: int(x), list(format(rule, '09b'))))
    rule_l.reverse()
    neighbours = set_neighbourhood(rule_l)
    for i in range(y):
        for j in range(x):
            cell = image[get_pos(j, i, x)]
            for x,y in neighbours:
                if check_in_bounds(j+x, i+y, x, y) and neighbours[ct] == 1:
                    neighbour = get_pos(j+x, i+y, x)
                    cell.append(neighbour)

def find_incoming_nodes(pos:int, image):
    nodes = []
    for i in range(len(image)):
        if pos in image[i]:
            nodes.append(i)
    
    return nodes

def find_chain(pos:int, cols:int, chain:list, frm:int, image):
    chain.append(print_cell(pos, cols))
    
    incoming = find_incoming_nodes(pos, image)
    incoming = [node for node in incoming if node is not frm]
    for node in incoming:
        outgoing = image[node]
        for n in outgoing:
            if n is image[pos]:
                find_chain(get_pos(n.j-1, n.i-1, x), cols, chain, node, image)

def find_max(rule: int, x, y, image, memory:dict):
    if(rule in memory.keys()):
        return memory[rule]
    
    maxx = 0
    longest_chain = []
    for i in range(y):
        for j in range(x):
            chain = []
            find_chain(get_pos(j, i, x), x, chain, None, image)
            if len(chain) > maxx:
                longest_chain = chain
                maxx = len(chain)
    
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
    longest_chain = []
    for r in comps:
        image = [[] for i in range(0,y) for j in range(0,x)]
        apply_rule(r, x, y, image)
        # print(*image, sep="\n")
        res = find_max(r, x, y, image, memory)
        if res[0] > m:
            m = res[0]
            longest_chain = res[1]
    return (m, longest_chain)

if __name__ == "__main__":
    y = int(input("Enter the number of rows:\t"))
    x = int(input("Enter the number of columns:\t"))
    rule = int(input("Enter the rule:\t"))
    m, chain = find_k(rule, x, y, {})
    print("Longest Chain:\t", chain)
    print("Value of k:\t", 2**math.ceil(math.log2(m)))
    
