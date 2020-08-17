def compute_opm(opm_list:list):
    try:
        drop = 0
        for i in range(1,len(opm_list)):
            if((opm_list[i-1]-opm_list[i])/max(abs(opm_list[i]),0.01)<-0.2):
                drop = 1
                break
        opm_sum = sum(opm_list)
        if(opm_sum<0 or opm_list[0]<0):
            return "C"
        elif(((opm_list[0]-opm_list[1])/max(abs(opm_list[1]),0.01))<-0.2 or (drop==0 and opm_sum<20)):
            return "B"
        elif(drop==1):
            return "BB"
        elif(opm_sum>60 or (opm_sum>=40 and opm_list[0]>opm_list[1] and opm_sum<=60)):
            return "AA"
        elif(opm_sum>40 or (opm_sum>=20 and opm_list[0]>opm_list[1] and opm_sum<=40)):
            return "A"
        else:
            return "BB"
        return "error"
    except:
        return "error"
def compute_niatgr(niatgr_list:list):
    try:
        list1 = []
        for i in range(0,4):
            list1.append((niatgr_list[i] - niatgr_list[i+4])/max(abs(niatgr_list[i+4]),0.01))
        negative = 0
        fifty = 0
        positive = 0
        for i in range(len(list1)):
            if(list1[i]<0):
                negative+=1
            if(list1[i]>50 and i!=len(list1)-1):
                fifty+=1
            if(list1[i]>=0 and i!=len(list1)-1):
                positive+=1

        if(list1[0]<0 and list1[1]<0):
            return "C"
        elif(list1[0]<0 or negative>=2 or (list1[0]<list1[1] and list1[1]<list1[2] and fifty==0)):
            return "B"
        elif((list1[0]>=0 and list1[1]>=0 and list1[1]-list1[0]>=max(abs(list1[1]),0.01)*0.5) or (list1[1]<0 and list1[0]>=0)):
            return "BB"
        elif((positive==3 and list1[0]>list1[1]) or fifty==3):
            return "AA"
        elif((list1[0]>=0 and list1[1]>=0 and list1[1]-list1[0]<max(abs(list1[1]),0.01)*0.5)):
            return "A"
        return "error"
    except:
        return "error"

def compute_eps(eps_list:list):
    try:
        eps_sum = sum(eps_list)
        if(eps_sum<0):
            return "C"
        elif(eps_list[0]<0):
            return "B"
        elif(eps_sum>=5):
            return "AA"
        elif(eps_sum>=3 and eps_sum<5):
            return "A"
        elif(eps_sum>=1 and eps_sum<3):
            return "BB"
        elif(eps_sum>=0):
            return "B"
        return "error"
    except:
        return "error"

def compute_it(it_list:list):
    try:
        drop = 0
        for i in range(1,len(it_list)):
            if(it_list[i]*0.2<it_list[i]-it_list[i-1]):
                drop+=1
        it_sum = sum(it_list)
        if(it_list.count(0.0)==4):
            return "N"
        elif(drop==0 and it_sum>=6):
            return "AA"
        elif(drop==0 and it_sum<6):
            return "A"
        elif(it_list[1]*0.2<it_list[1]-it_list[0]):
            return "C"
        elif(drop>=1):
            return "B"
        elif((it_list[0]>it_list[1] and it_list[1]>it_list[2] and (it_list[2]-it_list[0])/it_list[2]>0.2)):
            return "BB"
        elif((it_list[1]>it_list[2] and it_list[2]>it_list[3] and (it_list[3]-it_list[1])/it_list[3]>0.2)):
            return "BB"
        return "error"
    except:
        return "error"

def compute_argr(argr_list:list):
    try:
        negative = 0
        for i in range(len(argr_list)):
            if(argr_list[i]<0):
                negative +=1
        argr_sum = sum(argr_list)
        if(negative==0 and argr_sum>=150 and argr_list[0]>=argr_list[1]):
            return "AA"
        elif((negative==0 and argr_sum>=60 and argr_list[0]>=argr_list[1] and argr_sum<150) or (argr_sum>=150 and argr_list[1]-argr_list[0]<max(abs(argr_list[1]),0.01)*0.5)):
            return "A"
        elif(argr_sum<0 or argr_list[0]<0):
            return "C"
        elif(argr_sum>=0 and argr_list[0]<argr_list[1] and argr_list[1]<argr_list[2]):
            return "B"
        else:
            return "BB"
        return "error"
    except:
        return "error"

def compute_fcf(fcf_list:list):
    try:
        positive = 0
        for i in fcf_list:
            if(i>=0):
                positive+=1
        if(positive==6):
            return "AA"
        elif(sum(fcf_list)>=0):
            return "A"
        elif(sum(fcf_list[:4])>=0):
            return "BB"
        elif(sum(fcf_list[:4])<0):
            return "B"
        elif(sum(fcf_list)<0):
            return "C"
        return "error"
    except:
        return "error"