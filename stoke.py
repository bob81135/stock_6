from bs4 import BeautifulSoup
import requests
dict = {}
error = 0
name = ""
label_name = {'eps': '獲利能力(EPS)評分標準', 'opm': '營益率評分標準', 'niatgr': '稅後淨利年增率', 'it': '存貨周轉率', 'fcf': '自由現金流量評分標準', 'argr': '營收年增率'}
score = {"AA":5,"A":4,"BB":3,"B":2,"C":1}
def compute_opm(opm_list1:list):
    global error
    try:
        tag = opm_list1.parent.select('td')
        tag = tag[1:5]
        tag = [float(i.text.replace(",","")) for i in tag]
        drop = 0
        for i in range(1,len(tag)):
            if((tag[i-1]-tag[i])/max(abs(tag[i]),0.01)<-0.2):
                drop = 1
                break
        if(sum(tag)<0 or tag[0]<0):
            dict["opm"] = "C"
        elif(((tag[0]-tag[1])/max(abs(tag[1]),0.01))<-0.2 or (drop==0 and sum(tag)<20)):
            dict["opm"] = "B"
        elif(drop==1):
            dict["opm"] = "BB"
        elif(sum(tag)>60 or (sum(tag)>=40 and tag[0]>tag[1] and sum(tag)<=60)):
            dict["opm"] = "AA"
        elif(sum(tag)>40 or (sum(tag)>=20 and tag[0]>tag[1] and sum(tag)<=40)):
            dict["opm"] = "A"
        else:
            dict["opm"] = "BB"
    except:
        error = 1
        print(label_name["opm"]+"input data error")
def compute_niatgr(niatgr_list1:list):
    global error
    try:
        tag = niatgr_list1.parent.select('td')
        tag = tag[1:]
        tag = [float(i.text.replace(",","")) for i in tag]
        list1 = []
        for i in range(0,4):
            list1.append((tag[i] - tag[i+4])/max(abs(tag[i+4]),0.01))
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
            dict["niatgr"] = "C"
        elif(list1[0]<0 or negative>=2 or (list1[0]<list1[1] and list1[1]<list1[2] and fifty==0)):
            dict["niatgr"] = "B"
        elif((list1[0]>=0 and list1[1]>=0 and list1[1]-list1[0]>=max(abs(list1[1]),0.01)*0.5) or (list1[1]<0 and list1[0]>=0)):
            dict["niatgr"] = "BB"
        elif((positive==3 and list1[0]>list1[1]) or fifty==3):
            dict["niatgr"] = "AA"
        elif((list1[0]>=0 and list1[1]>=0 and list1[1]-list1[0]<max(abs(list1[1]),0.01)*0.5)):
            dict["niatgr"] = "A"
    except:
        error = 2
        print(label_name["niatgr"]+" input data error")

def compute_eps(eps_list1:list):
    global error
    try:
        tag = eps_list1.parent.select('td')
        tag = tag[1:5]
        tag = [float(i.text.replace(",","")) for i in tag]
        eps_sum = sum(tag)
        if(eps_sum<0):
            dict["eps"] = "C"
        elif(tag[0]<0):
            dict["eps"] = "B"
        elif(eps_sum>=5):
            dict["eps"] = "AA"
        elif(eps_sum>=3 and eps_sum<5):
            dict["eps"] = "A"
        elif(eps_sum>=1 and eps_sum<3):
            dict["eps"] = "BB"
        elif(eps_sum>=0):
            dict["eps"] = "B"
            
    except:
        error = 3
        print(label_name["eps"]+" input data error")

def compute_it(it_list1:list):
    global error
    try:
        tag = it_list1.parent.select('td')
        tag = tag[1:5]
        tag = [float(i.text.replace(",","")) for i in tag]
        drop = 0
        for i in range(1,len(tag)):
            if(tag[i]*0.2<tag[i]-tag[i-1]):
                drop+=1
        if(tag.count(0.0)==4):
            dict["it"] = "N"
        elif(drop==0 and sum(tag)>=6):
            dict["it"] = "AA"
        elif(drop==0 and sum(tag)<6):
            dict["it"] = "A"
        elif(tag[1]*0.2<tag[1]-tag[0]):
            dict["it"] = "C"
        elif(drop>=1):
            dict["it"] = "B"
        elif((tag[0]>tag[1] and tag[1]>tag[2] and (tag[2]-tag[0])/tag[2]>0.2)):
            dict["it"] = "BB"
        elif((tag[1]>tag[2] and tag[2]>tag[3] and (tag[3]-tag[1])/tag[3]>0.2)):
            dict["it"] = "BB"
    except:
        error = 4
        print(label_name["it"]+" input data error")
def argr_function(url):
    global error
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        argr = soup.find('td',string="年/月")
        argr_list1 = []
        negative = 0
        index = argr.parent
        for _ in range(6):
            index = index.next_sibling.next_sibling
            argr = float((index.select("td")[4].text.replace(",",""))[:-1])
            if(argr<0):
                negative +=1
            argr_list1.append(argr)
        if(negative==0 and sum(argr_list1)>=150 and argr_list1[0]>=argr_list1[1]):
            dict["argr"] = "AA"
        elif((negative==0 and sum(argr_list1)>=60 and argr_list1[0]>=argr_list1[1] and sum(argr_list1)<150) or (sum(argr_list1)>=150 and argr_list1[1]-argr_list1[0]<max(abs(argr_list1[1]),0.01)*0.5)):
            dict["argr"] = "A"
        elif(sum(argr_list1)<0 or argr_list1[0]<0):
            dict["argr"] = "C"
        elif(sum(argr_list1)>=0 and argr_list1[0]<argr_list1[1] and argr_list1[1]<argr_list1[2]):
            dict["argr"] = "B"
        else:
            dict["argr"] = "BB"
    except:
        error = 5
        print(label_name["argr"]+" input data error")
def fcf_function(url):
    global error
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        fcf = soup.find('td',string="來自營運之現金流量")
        if(fcf==None):
            fcf = soup.find('td',string=" 來自營運之現金流量")
        tag = fcf.parent.select('td')
        tag = tag[1:7]
        fcf_list1 = [float(i.text.replace(",","")) for i in tag]
        fcf = soup.find('td',string="投資活動之現金流量")
        if(fcf==None):
            fcf = soup.find('td',string=" 投資活動之現金流量")
        tag = fcf.parent.select('td')
        tag = tag[1:7]
        fcf_list1 = [float(tag[i].text.replace(",",""))+fcf_list1[i] for i in range(len(tag))]
        positive = 0
        for i in fcf_list1:
            if(i>=0):
                positive+=1
        if(positive==6):
            dict["fcf"] = "AA"
        elif(sum(fcf_list1)>=0):
            dict["fcf"] = "A"
        elif(sum(fcf_list1[:4])>=0):
            dict["fcf"] = "BB"
        elif(sum(fcf_list1[:4])<0):
            dict["fcf"] = "B"
        elif(sum(fcf_list1)<0):
            dict["fcf"] = "C"
    except:
        error = 6
        print(label_name["fcf"]+" input data error")
def main_function(url):
    global name
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    name = soup.title.text[:-7]
    eps = soup.find('td',string="每股盈餘")
    compute_eps(eps)
    opm = soup.find('td',string="營業利益率")
    if(opm==None):
        opm = soup.find('td',string="經常淨利成長率")
    compute_opm(opm)
    niatgr = soup.find('td',string="稅後淨利率")
    if(niatgr==None):
        niatgr = soup.find('td',string="稅後淨利率(A)")
    compute_niatgr(niatgr)
    it = soup.find('td',string="存貨週轉率(次)")
    if(it==None):
        dict["it"] = "N"
    else:
        compute_it(it)
while(1):
    dict = {}
    id = input("輸入股票代碼:")
    error = 0
    url = "https://jdata.yuanta.com.tw/z/zc/zcr/zcr_"+id+".djhtm"
    url1 = "https://jdata.yuanta.com.tw/z/zc/zc3/zc3_"+id+".djhtm"
    url2 = "https://jdata.yuanta.com.tw/z/zc/zch/zch_"+id+".djhtm"
    main_function(url)
    fcf_function(url1)
    argr_function(url2)
    if(error==0 and len(dict)==6):
        print(name)
        total_score = 0
        total_label = 0
        for i in label_name:
            print(label_name[i],":",dict[i])
            if(dict[i]!="N"):
                total_score+=score[dict[i]]
                total_label+=1
        print("total_score",":",round(total_score/total_label,1))
    else:
        print("have some data error")
 