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

    def get_probability(self, index): #return [選機,排序]
        
        if len(self.gene) > 0 and len(self.jobs) + index < len(self.gene):
            return self.gene[index], self.gene[len(self.jobs) + index]

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
        print(self.gene)
        return self.gene


    def clear_values(self):
        self.makespan=0
        self.tardiness_num=0


# Crossover
def Crossover(parent_list,offspring_list,population_size,jobs_size,crossover_rate):

    s=list(np.random.permutation(population_size)) #[0,2,3,1]
    #s=[0,1,2,3]
    for m in range(int(population_size/2)): #2
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob: 

            parent1= deepcopy(parent_list[s[2*m]].probability)
            parent2= deepcopy(parent_list[s[2*m+1]].probability)

            size=range(1,jobs_size*2 +1)  #染色體大小 #10+10(1~20)   #1~100 
            #test
            # size=range(1,7)  #6666666666666666666666

            CutPoint=random.sample(size, 2) 
            CutPoint.sort()
            #print(CutPoint)

            child1= deepcopy(parent1)
            child2= deepcopy(parent2)

            child1[CutPoint[0]-1:CutPoint[1]]=parent2[CutPoint[0]-1:CutPoint[1]]
            child2[CutPoint[0]-1:CutPoint[1]]=parent1[CutPoint[0]-1:CutPoint[1]]

            offspring_list[s[2*m]].probability = deepcopy(child1)
            offspring_list[s[2*m+1]].probability = deepcopy(child2)

    return offspring_list


# Mutation
def mutation(population_size,offspring_list,mutation_rate,jobs_size):

    s=list(np.random.permutation(population_size)) #[0,2,3,1]
    #print(s)
    for m in range(len(offspring_list)):
            mutation_prob=np.random.rand()
            if mutation_rate >= mutation_prob:
                
                size=range(0,jobs_size*2)  #染色體大小 #10+10(0~19)  #1~100 
                # #test
                # size=range(0,6)  #0-5  #6666666666666666666666
                one_gene=random.sample(size, 1) 
                #print("第",m+1,"次",one_gene[0])
                offspring_list[s[m]].probability[one_gene[0]] = random.random()

    return offspring_list

# rank_selection

def rank_selection_get_proba_list(rank_selection_size):

    def sum(num): #分母
        sum = 0
        x=1
        while x < num+1:
            sum = sum + x
            x+=1
        return sum
    Sum=sum(rank_selection_size) #1+2+..+18

    t=0
    proba_list=[0]
    for i in range(rank_selection_size-1):
        proba=(rank_selection_size-i)/Sum #90/1+...
        t+=proba
        proba_list.append(t)
    
    return proba_list

def rank_selection_get_select_index(proba_list,rank_selection_num):

    def getk2(): #得index
        selectone=random.random()
        k2=-1
        for i in range(len(proba_list)):
            if(selectone>proba_list[i]):
                k2+=1
        return k2

    select_index=[]
    count=0
    while(len(select_index)<rank_selection_num): #不重複 #40個
        count+=1
        temp=getk2()
        if(temp not in select_index):
            select_index.append(temp)
    
    return select_index

