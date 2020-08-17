from bs4 import BeautifulSoup
import requests
import financial_index
dict = {}
error = 0
name = ""
label_name = {'eps': '獲利能力(EPS)評分標準', 'opm': '營益率評分標準', 'niatgr': '稅後淨利年增率', 'it': '存貨周轉率', 'fcf': '自由現金流量評分標準', 'argr': '營收年增率'}
score = {"AA":5,"A":4,"BB":3,"B":2,"C":1}

def fcf_function(url):
    global error
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        fcf = soup.find('td',string="來自營運之現金流量")
        if(fcf==None):
            fcf = soup.find('td',string=" 來自營運之現金流量")
        fcf_list = fcf.parent.select('td')
        fcf_list = [float(i.text.replace(",","")) for i in fcf_list[1:7]]
        fcf = soup.find('td',string="投資活動之現金流量")
        if(fcf==None):
            fcf = soup.find('td',string=" 投資活動之現金流量")
        fcf_list1 = fcf.parent.select('td')
        fcf_list1 = fcf_list1[1:7]
        fcf_list = [float(fcf_list1[i].text.replace(",",""))+fcf_list[i] for i in range(len(fcf_list1))]
        fcf_ans = financial_index.compute_fcf(fcf_list)
        if(fcf_ans=="error"):
            error = 6
            print(label_name["fcf"]+" input data error")
        else:
            dict["fcf"] = fcf_ans
    except:
        error = 6
        print(label_name["fcf"]+" input data error")

def argr_function(url):
    global error
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        argr = soup.find('td',string="年/月")
        argr_list = []
        index = argr.parent
        for _ in range(6):
            index = index.next_sibling.next_sibling
            argr = float((index.select("td")[4].text.replace(",",""))[:-1])
            argr_list.append(argr)
        argr_ans = financial_index.compute_argr(argr_list)
        if(argr_ans=="error"):
            error = 5
            print(label_name["argr"]+" input data error")
        else:
            dict["argr"] = argr_ans
    except:
        error = 5
        print(label_name["argr"]+" input data error")

def main_function(url):
    global name,error
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    if(len(soup.title.text)>7):
        name = soup.title.text[:-7]
    try:
        eps = soup.find('td',string="每股盈餘")
        eps_list = eps.parent.select('td')
        eps_list = [float(i.text.replace(",","")) for i in eps_list[1:5]]
        eps_ans = financial_index.compute_eps(eps_list)
        if(eps_ans=="error"):
            error = 1
            print(label_name["eps"]+" input data error")
        else:
            dict["eps"] = eps_ans
    except:
        error = 1
        print(label_name["eps"]+" input data error")

    try:
        opm = soup.find('td',string="營業利益率")
        if(opm==None):
            opm = soup.find('td',string="經常淨利成長率")
        opm_list = opm.parent.select('td')
        opm_list = [float(i.text.replace(",","")) for i in opm_list[1:5]]
        opm_ans = financial_index.compute_opm(opm_list)
        if(opm_ans=="error"):
            error = 2
            print(label_name["opm"]+"input data error")
        else:
            dict["opm"] = eps_ans
    except:
        error = 2
        print(label_name["opm"]+"input data error")

    try:
        niatgr = soup.find('td',string="稅後淨利率")
        if(niatgr==None):
            niatgr = soup.find('td',string="稅後淨利率(A)")
        niatgr_list = niatgr.parent.select('td')
        niatgr_list = [float(i.text.replace(",","")) for i in niatgr_list[1:]]
        niatgr_ans = financial_index.compute_niatgr(niatgr_list)
        if(niatgr_ans=="error"):
            error = 3
            print(label_name["niatgr"]+" input data error")
        else:
            dict["niatgr"] = niatgr_ans
    except:
        error = 3
        print(label_name["niatgr"]+" input data error")
    try:
        it = soup.find('td',string="存貨週轉率(次)")
        if(it==None):
            dict["it"] = "N"
        else:
            it_list = it.parent.select('td')
            it_list = [float(i.text.replace(",","")) for i in it_list[1:5]]
            it_ans = financial_index.compute_it(it_list)
            if(it_ans=="error"):
                error = 4
                print(label_name["it"]+" input data error")
            else:
                dict["it"] = it_ans
    except:
        error = 4
        print(label_name["it"]+" input data error")
    
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
 