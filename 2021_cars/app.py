import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
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
                temp.append((data['label'], data['weight'], data['time']))
        if len(temp) == 0:
            continue
        temp.sort(key=lambda data: data[1])

        # thres = 10000
        # if len(temp) >= 1:
        #     thres = temp[0][1]/temp[1][1]

        for s, w, t in temp:
            # if w > thres:
            #     sol[i].append((s,2))
            # else:
            sol[i].append((s,int(w/11) + 1))

    return sol

def solve_time(G, I):
    sol = {}
    for i in range(I):
        sol[i] = []
        temp = []
        for u, v, data in G.in_edges(i, data=True):
            if data['weight'] > 0:
                temp.append((data['label'], data['weight'], data['time']))
        if len(temp) == 0:
            continue
        temp.sort(key=lambda data: data[1])

        # thres = 10000
        # if len(temp) >= 1:
        #     thres = temp[0][1]/temp[1][1]

        for s, w, t in temp:
            if w > 0:
                c = 1
                # if t > 4:
                #     c += 1
                if w > temp[int(len(temp)/2)][1]:
                    c += 1
                sol[i].append((s,c))

    return sol

def solve_e(G, I):
    sol = {}
    for i in range(I):
        sol[i] = []
        temp = []
        for u, v, data in G.in_edges(i, data=True):
            if data['weight'] > 0:
                temp.append((data['label'], data['weight'], data['time']))
        if len(temp) == 0:
            continue
        # temp.sort(key=lambda data: data[1])

        # thres = 10000
        # if len(temp) >= 1:
        #     thres = temp[0][1]/temp[1][1]
        charge = 0
        for s, w, t in temp:
            if w == 0:
                continue
            charge += w
        
        cst = charge / len(temp)

        for s, w, t in temp:
            if w <= 0:
                continue
            sol[i].append((s, min(2,int((w / 10) + 1))))

    return sol

solver = solve_time

def read_dataset(dataset_path):
    with open(f"input/{dataset_path}.txt") as f:
        """
        D duration
        I nb intersection
        S b streets
        V nb cars
        F points for each cars
        """
        D,I,S,V,F = [int(s) for s in f.readline().split()]
        streets = []
        for i in range(S):
            """
            B : intersection at begining
            E : intersection at end
            L : length
            """
            B,E, name, L = [(s) for s in f.readline().split()]
            B,E,L = [int(s) for s in (B,E,L)]
            streets.append((B,E, name, L))
        cars = []
        for i in range(V):
            streets_names = f.readline().split()[1:]
            cars.append(streets_names)
            
        return D,I,S,V,F, streets, cars
    
def create_graph(I, streets):
    G=nx.DiGraph()
    G.add_nodes_from(range(I))
    for s in tqdm(streets):
        G.add_edge(s[0], s[1])
        G[s[0]][s[1]]['label'] = s[2]
        G[s[0]][s[1]]['time'] = s[3]
        G[s[0]][s[1]]['weight'] = s[3]
    return G

def street_weights(G, cars, streets):
    s2id = {}
    for s in streets:
        s2id[s[2]] = (s[0], s[1])
    for trajectory in cars:
        for s in trajectory:
            a, b = s2id[s]
            G[a][b]['weight'] -= 1


def write_output(sol, output_name):
    """
    sol = dict(intersectionID -> list(streetName, time T))
    """
    to_del = []
    for intID, schedule in sol.items():
        if len(schedule) == 0:
            to_del.append(intID)
    for i in to_del:
        del sol[i]
    
    with open(f"output/{output_name}_out.txt", 'w') as f:
        n = len(sol)
        f.write(f'{n}\n')
        for intID, schedule in sol.items():
            f.write(f'{intID}\n')
            f.write(f'{len(schedule)}\n')
            for street, time in schedule:
                f.write(f'{street} {time}\n')


def solve(G, I):
    return solver(G,I)


if __name__ == "__main__":
    filenames = ['a', 'b', 'c', 'd', 'e', 'f']
    # filenames = ['c']

    for filename in filenames:
        print(f"Processing dataset {filename}")
        D,I,S,V,F, streets, cars = read_dataset(filename)
        G = create_graph(I, streets)
        # nx.draw(G)
        # plt.savefig("f.png")
        # plt.show()

        street_weights(G, cars, streets)
        sol = solve(G, I)
        write_output(sol, filename)