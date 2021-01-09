from stock_6.processor.stoke import stock
import os, csv
import time

def main():
    # with open('./data/150.txt') as f:
    #     lines = f.read().splitlines()
    input_name = input("輸入input的csv檔案名稱")
    output_name = input("輸入output的csv檔案名稱")
    with open(os.getcwd() + '/' + output_name + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['股票編號', '股票名稱', '營益率評分標準', '營收年增率', '稅後淨利年增率', '自由現金流量評分標準', '獲利能力(EPS)評分標準', '存貨周轉率', '得分'])
    with open(os.getcwd() + '/' + input_name + '.csv', 'r') as f:
        rows = csv.DictReader(f)
        for row in rows:
            result = stock(row['股票編號'], row['股票名稱'])
            with open(os.getcwd() + '/' + output_name + '.csv', 'a') as f:
                writer = csv.writer(f)
                if (result[0] == "error"):
                    writer.writerow([row['股票編號'], row['股票名稱']])
                else:
                    writer.writerow(result)

            time.sleep(2)

if __name__ == '__main__':
	sys.exit(main())
