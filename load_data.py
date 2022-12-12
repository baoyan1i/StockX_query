from elasticsearch import Elasticsearch
import csv

es = Elasticsearch(['http://localhost:9200'])

with open("/Users/baoyanli/Downloads/StockX-Data-Contest-2019-3.csv", "r") as f:
    reader = csv.reader(f)

    for i, line in enumerate(reader):
        tmp = []
        sale_price = []
        str_price = ""
        price = 0
        for item in line[3]:

            for i in item:
                if i.isdigit():

                    str_price = str_price + i
                    price = int(str_price)
            sale_price.append(price)




        document = {
            "Brand": line[1],
            "Sneaker Name": line[2],
            "Sale Price": line[3],
            "Retail Price": line[4],
        }
        # es.index(index="stockx1", document=document)
        print(sale_price[-1])
