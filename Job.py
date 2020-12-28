import re
class Job():
    def __init__(self, configure,eqp_recipe): #processTime=eqp
        self.configure = configure

        for i in self.configure.index:   #LOT_ID、OPE_NO... to object
            setattr(self, i, self.configure[i])
        self.processTime = eqp_recipe[eqp_recipe["RECIPE"] == self.configure["RECIPE"]] #一張表 #filter to recipe #Y8000
        self.canRunMachine=[]
        self.canRunMachine_num =0
        self.generate_canrunM()
        self.arrive_time= float(self.configure["ARRIV_T"])

        self.machineID = ''  #var
        self.order = 0  #var
        self.startTime = 0 #var
        self.endTime = 0 #var
        self.genes = []

    def generate_canrunM(self):
        allM=self.configure["CANRUN_TOOL"]

        def cut_text(text,lenth):
            textArr = re.findall('.{'+str(lenth)+'}', text)
            textArr.append(text[(len(textArr)*lenth):])
            return textArr

        self.canRunMachine=cut_text(allM,6)[:-1] #長度6 多餘-1
        #print(self.canRunMachine)
        self.canRunMachine_num = len(self.canRunMachine)

        return self.canRunMachine

    #
    def set_gene(self, genes): #genes=[選機,排序]
        self.genes = genes 
        # set machine
        self.machineID = self.canRunMachine[self.genes[0]-1]
        # set order
        self.order = self.genes[1]
 
        return self.machineID,self.order


    def set_start_time(self, time):
        self.startTime = self.arrive_time
        if time >= self.startTime:
            self.startTime = round(time,0)
        processTime = int(self.processTime[ self.processTime["EQP_ID"] == self.machineID ]["PROCESS_TIME"]) *  int(self.configure["QTY"])/25  #!
        self.endTime = round(self.startTime + processTime,0)

    def get_end_time(self):
        return self.endTime



