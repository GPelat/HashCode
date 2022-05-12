from audioop import reverse
from tqdm import tqdm
from collections import defaultdict
import numpy as np

class project:
    def __init__(self, name, d, s, b, skills):
        self.name = name
        self.d = d
        self.s = s
        self.b = b
        self.skills = skills
        self.score = s*len(skills)


class contributeur:
    def __init__(self, name, skills):
        self.name = name
        self.d = 0
        self.skills = skills
        self.skillsum = 0
        for key in skills:
            self.skillsum += skills[key]
        

def read_dataset(dataset_path):
    with open(f"input/{dataset_path}.in.txt") as f:
        """
        C n_contributors
        P n_projects
        """
        C, P = [int(s) for s in f.readline().split()]
        contributors = []
        for i in range(C):
            name, N = [(s) for s in f.readline().split()]
            N = int(N)
            skills = defaultdict(lambda:0)
            for j in range(N):
                skill, lvl = [(s) for s in f.readline().split()]
                lvl = int(lvl)
                skills[skill] = lvl
            contributors.append(contributeur(name,skills))

        projects = []
        for i in range(P):
            name, D, S, B, R = [(s) for s in f.readline().split()]
            D, S, B, R = [int(s) for s in (D,S,B,R)]
            skills = []
            for j in range(R):
                skill, lvl = [(s) for s in f.readline().split()]
                lvl = int(lvl)
                skills.append((skill, lvl))
            projects.append(project(name,D,S,B,skills))
        return contributors, projects


def write_output(sol, output_name):
    """
    sol = dict(intersectionID -> list(streetName, time T))
    """    
    with open(f"output/{output_name}_out.txt", 'w') as f:
        n = len(sol)
        f.write(f'{n}\n')
        for name, gens in sol.items():
            f.write(f'{name}\n')
            f.write(f"{' '.join(gens)}\n")

def duree(p):
    return p.d

def tempslibre(c):
    return c.skillsum

def is_mentor(cs, list_cs, skill):
    for i in list_cs:
        if cs[i].skills[skill[0]] >= skill[1]:
            return True
    return False


def solve(contributors, projects):
    sol = {}
    projects.sort(key=duree)
    done = [False for _ in projects]
    donethistime = 1
    r = 4
    while donethistime:
        donethistime = 0
        # print(done)
        for iter, p in tqdm(enumerate(projects), total=len(projects)):
            if done[iter]:
                continue
            contribs = []
            contribs_selected = []
            contributors.sort(key=tempslibre)
            for skill in p.skills:
                stop = False
                gotit = False
                for i, c in enumerate(contributors):
                    if (c.name not in contribs) and (c.skills[skill[0]] == skill[1]-1) and (is_mentor(contributors, contribs_selected, skill)):
                        if (p.b + p.s < c.d):
                            stop = True
                            break
                        contribs.append(c.name)
                        contribs_selected.append(i)
                        gotit = True
                        break
                if not gotit:
                    for i, c in enumerate(contributors):
                        if (c.name not in contribs) and (c.skills[skill[0]] >= skill[1]):
                            if (p.b + p.s < c.d):
                                stop = True
                                break
                            contribs.append(c.name)
                            contribs_selected.append(i)
                            break
                if stop:
                    break
            if len(contribs) == len(p.skills) and (p.b + p.s > contributors[contribs_selected[0]].d):
                donethistime += 1
                sol[p.name] = contribs
                done[iter] = True
                for i in contribs_selected:
                    contributors[i].d += p.d
                for i, j in enumerate(contribs_selected):
                    if contributors[j].skills[p.skills[i][0]] <= p.skills[i][1]:
                        contributors[j].skills[p.skills[i][0]] += 1
            if (len(contribs_selected)) and (p.b + p.s < contributors[contribs_selected[0]].d):
                done[iter] = True

    return sol

def solve_e(contributors, projects):
    sol = {}
    projects.sort(key=duree)
    for p in tqdm(projects):
        contribs = []
        contribs_selected = []
        for skill in p.skills:
            for i, c in enumerate(contributors):
                if (c.name not in contribs) and (c.skills[skill[0]] == skill[1]-1) and (is_mentor(contributors, contribs_selected, skill)):
                        contribs.append(c.name)
                        contribs_selected.append(i)
                        break
                if skill[0] in c.skills and c.name not in contribs and (c.skills[skill[0]] > skill[1]-1) :
                    contribs.append(c.name)
                    contribs_selected.append(i)
                    break
        if len(contribs) == len(p.skills):
            sol[p.name] = contribs

    return sol

def solve_f(contributors, projects):
    sol = {}
    projects.sort(key=duree)
    done = 1
    while done > 0:
        done = 0
        for p in tqdm(projects):
            if p.name in sol:
                continue
            contribs = []
            contributors.sort(key = tempslibre, reverse=True)
            contribs_selected = []
            for skill in p.skills:
                for i, c in enumerate(contributors):
                    if (c.name not in contribs) and (c.skills[skill[0]] == skill[1]-1) and (is_mentor(contributors, contribs_selected, skill)):
                            contribs.append(c.name)
                            contribs_selected.append(i)
                            break
                    if skill[0] in c.skills and c.name not in contribs and (c.skills[skill[0]] > skill[1]-1) :
                        contribs.append(c.name)
                        contribs_selected.append(i)
                        break
            if len(contribs) == len(p.skills):
                sol[p.name] = contribs
                done += 1 

    return sol

if __name__ == "__main__":
    filenames = ['b_better_start_small', 'c_collaboration', 'd_dense_schedule', 'f_find_great_mentors']
    # filenames = ['a_an_example']
    # filenames = ['b_better_start_small']
    # filenames = ['c_collaboration']
    # filenames = ['d_dense_schedule']
    # filenames = ['e_exceptional_skills']
    # filenames = ['f_find_great_mentors']

    for filename in filenames:
        print(f"Processing dataset {filename}")
        contributors, projects = read_dataset(filename)
        sol = solve_f(contributors, projects)
        write_output(sol, filename)