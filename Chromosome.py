import random
import numpy as np 
from copy import deepcopy

class Chromosome():
    def __init__(self,jobs):
        self.gene=[]
        self.jobs = jobs
   
        self.generate_gene()
        self.makespan=0
        self.tardiness_num=0
        self.target_value=0

    def __str__(self): #須為字串str
        return self.gene

    def generate_gene(self):

        # MS
        for i in range(len(self.jobs)): #
            size=range(1,self.jobs[i].canRunMachine_num+1)  #染色體大小 #10+10(0~19)  #1~100 
            one_gene=random.sample(size, 1) 
            self.gene.append(one_gene[0])

        # OS
        size=range(1,len(self.jobs)+1) 
        OS_gene=random.sample(size,len(self.jobs)) 
        self.gene.extend(OS_gene)
        #print(self.gene)

        return self.gene

    def get_gene(self, index): #return [選機,排序]
        
        #if len(self.gene) > 0 and len(self.jobs) + index < len(self.gene):
        return self.gene[index], self.gene[len(self.jobs) + index]


    def clear_values(self):
        self.makespan=0
        self.tardiness_num=0


# Crossover
def Crossover(parent_list,offspring_list,population_size,jobs_size,crossover_rate):

    s=list(np.random.permutation(population_size)) #[0,2,3,1]
    #s=[0,1,2,3]
    for m in range(int(population_size/2)): #2
        crossover_prob=np.random.rand()
        if crossover_rate >= crossover_prob: 
            parent1= deepcopy(parent_list[s[2*m]].gene)
            parent2= deepcopy(parent_list[s[2*m+1]].gene)

            # MS
            size=range(1,jobs_size +1)  

            CutPoint=random.sample(size, 2) 
            CutPoint.sort()

            child_M1= deepcopy(parent1[:jobs_size])
            child_M2= deepcopy(parent2[:jobs_size])

            child_M1[CutPoint[0]-1:CutPoint[1]]=parent2[CutPoint[0]-1:CutPoint[1]]
            child_M2[CutPoint[0]-1:CutPoint[1]]=parent1[CutPoint[0]-1:CutPoint[1]]

            # OS
            child_O1= deepcopy(parent1[jobs_size:])
            child_O2= deepcopy(parent2[jobs_size:])

            allset=set([i+1 for i in range(jobs_size)])
            size=range(1,jobs_size+1) 
            choosenum= random.randrange(1, jobs_size, 1)
            jobset1=set(random.sample(size,choosenum)) 
            jobset2=jobset1 ^ allset

            for i in range(jobs_size):
                if child_O1[i] not in jobset1:
                    child_O1[i]=0
                if child_O2[i] not in jobset1:
                    child_O2[i]=0

            c1=[parent2[jobs_size:][i] for i in range(jobs_size) if parent2[jobs_size:][i] in jobset2]
            c2=[parent1[jobs_size:][i] for i in range(jobs_size) if parent1[jobs_size:][i] in jobset2]

            for i in range(len(jobset2)):
                child_O1[child_O1.index(0)]=c1[i]
                child_O2[child_O2.index(0)]=c2[i]

            # combine
            child_M1.extend(child_O1)
            child_M2.extend(child_O2)

            offspring_list[s[2*m]].gene = deepcopy(child_M1)
            offspring_list[s[2*m+1]].gene = deepcopy(child_M2)
       
    return offspring_list


# Mutation
def mutation(population_size,offspring_list,mutation_rate,jobs):
    jobs_size = len(jobs)
    s=list(np.random.permutation(population_size)) #[0,2,3,1]
    #print(s)
    for m in range(len(offspring_list)):
            mutation_prob=np.random.rand()
            if mutation_rate >= mutation_prob:
                # MS
                r= int(jobs_size/2)
                size=range(0,jobs_size)  
                choose_gene=random.sample(size, r) 
                choose_gene.sort()
                #print("原本:",offspring_list[s[m]].gene)
                for i in range(len(choose_gene)):
                    canRunMachine_size=range(1,jobs[choose_gene[i]].canRunMachine_num + 1)
                    new_gene = offspring_list[s[m]].gene[choose_gene[i]]
                    while new_gene == offspring_list[s[m]].gene[choose_gene[i]]:
                        new_gene=random.sample(canRunMachine_size, 1)[0]
                    #print("新:",new_gene)
                    offspring_list[s[m]].gene[choose_gene[i]] = new_gene

                #print("MS後:",offspring_list[s[m]].gene)
                #offspring_list[s[m]].gene[one_gene[0]] = random.random()

                # OS
                size=range(jobs_size,jobs_size*2)  
                SwappingPoint=random.sample(size, 2)
                #print(SwappingPoint)
                offspring_list[s[m]].gene[SwappingPoint[0]],offspring_list[s[m]].gene[SwappingPoint[1]] = offspring_list[s[m]].gene[SwappingPoint[1]] ,offspring_list[s[m]].gene[SwappingPoint[0]]
                #print("OS後:",offspring_list[s[m]].gene)

    return offspring_list

# Tournament_selection

def Tournament_selection_get_select_index(sorted_total_chromosomes,rank_selection_num,population_size,elite_selection_size):

    size=range(elite_selection_size,population_size*2)  
    choosegenlist=random.sample(size, rank_selection_num*2)

    select_index=[]
    for m in range(rank_selection_num): #8
        t1= sorted_total_chromosomes[choosegenlist[2*m]].target_value
        t2= sorted_total_chromosomes[choosegenlist[2*m+1]].target_value
        # print(t1,choosegenlist[2*m])
        # print(t2,choosegenlist[2*m+1])
        # print("-----")
        if t1 < t2:
            select_index.append(choosegenlist[2*m])
        else:
            select_index.append(choosegenlist[2*m+1])
        # print(select_index)
    return select_index

