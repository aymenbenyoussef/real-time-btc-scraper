import pandas as pd 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time 
import csv
import os

url = "https://coinmarketcap.com/"

file_path = r"C:\Users\HP\Desktop\Nouveau dossier\python\Data Scraping\Bitcoin_currency.csv"

page = requests.get(url)

soup=BeautifulSoup(page.text,"html.parser")

table = soup.find('table',class_="sc-7b3ac367-3 etbcea cmc-table")#sc-7b3ac367-3 etbcea cmc-table"

columns = table.find_all('th')#find_all('th')

columns_header = [head.text for head in columns[2:-1]]
    
columns_header.append("Date")

columns_header.append("Hour")

df = pd.DataFrame(columns=columns_header)

if not os.path.exists(file_path):
    df.to_csv(file_path)

def Scrap_b():

    today = datetime.now().strftime("%Y-%m-%d")

    hour = datetime.now().strftime("%H:%M")
    
    url = "https://coinmarketcap.com/"

    page = requests.get(url)

    soup=BeautifulSoup(page.text,"html.parser")

    table = soup.find('table',class_="sc-7b3ac367-3 etbcea cmc-table")

    columns = table.find_all('th')
    
    table_rows = table.find_all('tr')

    for row in table_rows[1:2]:

        data_row = row.find_all('td')
        
        row_data = [ data.text for data in data_row[2:-1]]
        
        row_data.append(today)

        row_data.append(hour)
        
        #row_data.insert(0,len(df))
        i = 2
        for td in data_row[4:7]:
            
            span = td.find_all('span')

            for sp in span[:-1]:
                
                xp = sp.find_all('span')

                for x in xp:
                    a = x.get('class')
                    check = a[0][11:]
                    if check=="down":
                        row_data[i] = "down "+row_data[i]
                    else:
                        row_data[i] = "up "+row_data[i]
                    i+= 1   

    
    try:
        df.loc[len(df)] = row_data
    except Exception as e :
        raise e
        
    with open(file_path,"a+",newline="") as f:
        writer = csv.writer(f)
        df_2 = pd.read_csv(file_path)
        row_data.insert(0,len(df_2)+1)
        writer.writerow(row_data)
while(True):
    Scrap_b()
    time.sleep(60)
