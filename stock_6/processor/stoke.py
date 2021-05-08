import requests

from bs4 import BeautifulSoup
from stock_6.processor import financial_index

label_name = {
    'opm': '營益率評分標準',
    'argr': '營收年增率',
    'niatgr': '稅後淨利年增率',
    'fcf': '自由現金流量評分標準',
    'eps': '獲利能力(EPS)評分標準',
    'it': '存貨周轉率',
}
score = {"AA": 4, "A": 3, "BB": 2, "B": 1, "C": 0}

class Processor():
    def __init__(self):
        self.error_code = False
        self.data = dict()
        self.stock_name = None

    def process_fcf(self, url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            fcf = soup.find('td', string="來自營運之現金流量")
            if (fcf == None):
                fcf = soup.find('td', string=" 來自營運之現金流量")
            fcf_list = fcf.parent.select('td')
            fcf_list = [float(i.text.replace(",", "")) for i in fcf_list[1:7]]
            fcf = soup.find('td', string="投資活動之現金流量")
            if (fcf == None):
                fcf = soup.find('td', string=" 投資活動之現金流量")
            fcf_list1 = fcf.parent.select('td')
            fcf_list1 = fcf_list1[1:7]
            fcf_list = [
                float(fcf_list1[i].text.replace(",", "")) + fcf_list[i]
                for i in range(len(fcf_list1))
            ]
            fcf_ans = financial_index.compute_fcf(fcf_list)
            if (fcf_ans == "error"):
                self.error_code = True
                print(label_name["fcf"] + " input data error")
            else:
                self.data["fcf"] = fcf_ans
        except:
            self.error_code = True
            print(label_name["fcf"] + " input data error")

    def process_argr(self, url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            argr = soup.find('td', string="年/月")
            argr_list = []
            index = argr.parent
            for _ in range(6):
                index = index.next_sibling.next_sibling
                argr = float((index.select("td")[4].text.replace(",", ""))[:-1])
                argr_list.append(argr)
            argr_ans = financial_index.compute_argr(argr_list)
            if (argr_ans == "error"):
                self.error_code = True
                print(label_name["argr"] + " input data error")
            else:
                self.data["argr"] = argr_ans
        except:
            self.error_code = True
            print(label_name["argr"] + " input data error")

    def process_data(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        if (len(soup.title.text) > 7):
            self.stock_name = soup.title.text[:-7]
        try:
            eps = soup.find('td', string="每股盈餘")
            eps_list = eps.parent.select('td')
            eps_list = [float(i.text.replace(",", "")) for i in eps_list[1:5]]
            eps_ans = financial_index.compute_eps(eps_list)
            if (eps_ans == "error"):
                self.error_code = True
                print(label_name["eps"] + " input data error")
            else:
                self.data["eps"] = eps_ans
        except:
            self.error_code = True
            print(label_name["eps"] + " input data error")

        try:
            opm = soup.find('td', string="營業利益率")
            if (opm == None):
                opm = soup.find('td', string="經常淨利成長率")
            opm_list = opm.parent.select('td')
            opm_list = [float(i.text.replace(",", "")) for i in opm_list[1:5]]
            print(opm_list)
            opm_ans = financial_index.compute_opm(opm_list)
            if (opm_ans == "error"):
                self.error_code = True
                print(label_name["opm"] + "input data error")
            else:
                self.data["opm"] = opm_ans
        except:
            self.error_code = True
            print(label_name["opm"] + "input data error")

        try:
            niatgr = soup.find('td', string="稅後淨利率")
            if (niatgr == None):
                niatgr = soup.find('td', string="稅後淨利率(A)")
            niatgr_list = niatgr.parent.select('td')
            niatgr_list = [float(i.text.replace(",", "")) for i in niatgr_list[1:]]
            niatgr_ans = financial_index.compute_niatgr(niatgr_list)
            if (niatgr_ans == "error"):
                self.error_code = True
                print(label_name["niatgr"] + " input data error")
            else:
                self.data["niatgr"] = niatgr_ans
        except:
            self.error_code = True
            print(label_name["niatgr"] + " input data error")
        try:
            it = soup.find('td', string="存貨週轉率(次)")
            if (it is None):
                self.data["it"] = "N"
            else:
                it_list = it.parent.select('td')
                it_list = [float(i.text.replace(",", "")) for i in it_list[1:5]]
                it_ans = financial_index.compute_it(it_list)
                if (it_ans == "error"):
                    self.error_code = True
                    print(label_name["it"] + " input data error")
                else:
                    self.data["it"] = it_ans
        except:
            self.error_code = True
            print(label_name["it"] + " input data error")

def stock(stock_id, stock_name):
    # stock_id = input("輸入股票代碼:")
    url = "https://jdata.yuanta.com.tw/z/zc/zcr/zcr_" + stock_id + ".djhtm"
    url1 = "https://jdata.yuanta.com.tw/z/zc/zc3/zc3_" + stock_id + ".djhtm"
    url2 = "https://jdata.yuanta.com.tw/z/zc/zch/zch_" + stock_id + ".djhtm"

    processor = Processor()
    processor.process_data(url)
    processor.process_fcf(url1)
    processor.process_argr(url2)

    if (processor.error_code is False and len(processor.data) == 6):
        print(stock_name)
        csv_list = []
        csv_list.append(stock_id)
        csv_list.append(stock_name)
        total_score = 0
        total_label = 0
        for i in label_name:
            print(label_name[i], ":", processor.data[i])
            csv_list.append(processor.data[i])
            if (processor.data[i] != "N"):
                total_score += score[processor.data[i]]
                total_label += 1
        csv_list.append(round(total_score / total_label, 1))
        print("total_score", ":", round(total_score / total_label, 1))
        return csv_list
    else:
        print("have some data error")
        return ["error"]
        