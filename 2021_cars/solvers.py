import networkx as nx
import numpy as np

def solve_base(G, I):
    sol = {}
    for i in range(I):
        best = 0
        best_names = []
        names = []
        sol[i] = []
        for u, v, data in G.in_edges(i, data=True):
            if data['weight'] > best:
                best = data['weight']
                best_names = [data['label']]
            elif data['weight'] > best:
                best_names.append(data['label'])
            if data['weight'] > 0:
                names.append(data['label'])
        for s in best_names:
            sol[i].append((s,2))
        for s in names:
            if s not in best_names:
                sol[i].append((s,1))
    return sol

def solve_threshold(G, I):
    sol = {}
    for i in range(I):
        sol[i] = []
        temp = []
        for u, v, data in G.in_edges(i, data=True):
            if data['weight'] > 0:
                temp.append((data['label'], data['weight']))
        if len(temp) == 0:
            continue
        temp.sort(key=lambda data: data[1])

        # thres = 10000
        # if len(temp) >= 1:
        #     thres = temp[0][1]/temp[1][1]

        for s, w in temp:
            # if w > thres:
            #     sol[i].append((s,2))
            # else:
            sol[i].append((s,int(w/13) + 1))
    return sol

solver = solve_threshold