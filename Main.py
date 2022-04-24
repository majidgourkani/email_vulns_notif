import Output_gerenator
import Email_sender
from bs4 import BeautifulSoup
import requests
import sys
import schedule
import os.path
from datetime import datetime

def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk

def search(list_vuln, key_srch):
    tmp = []
    for k in key_srch:
        for x in list_vuln:
            if (k in x[1]) and (x not in tmp):
                tmp.append(x)
    return tmp

def Key_fetch():
    file_k = open("Keys.txt", "r")
    keys = file_k.read().splitlines()
    return keys

def Vuln_extractor(soup, list_vuln):
    levels = ["High Vulnerabilities", "Medium Vulnerabilities", "Low Vulnerabilities", "Severity Not Yet Assigned"]
    for l in levels:
        results = soup.find(summary=l)
        tmp = results.find_all("td")
        chnk_vl = list(list_split(tmp, 5))
        
        for i in range(len(chnk_vl)):
            tmp_l = [l.split()[0]]
            for j in range(len(chnk_vl[i])):
                if j==4:
                    tmp_l.append(chnk_vl[i][j].find('a',href=True).get_text())
                    tmp_l.append(chnk_vl[i][j].find('a',href=True)['href'])
                    continue
                tmp_l.append(chnk_vl[i][j].get_text())
            list_vuln.append(tmp_l)

def Latest_link():
    Base_url = "https://www.cisa.gov/uscert/ncas/bulletins"
    page = requests.get(Base_url)
    soup = BeautifulSoup(page.content, "html.parser")
    Last_link = "https://www.cisa.gov/uscert"+soup.find("div" , {"class","item-list"}).find_all("span")[0].find('a')['href']
    Link_desc = soup.find("div" , {"class","item-list"}).find_all("span")[0].text
    return Last_link, Link_desc

def Scheduled_task():
    list_vuln = []
    keys = []
    results_vuln = []
    url, desc = Latest_link()
    if os.path.isfile("outputs/{}.html".format(desc.split(":")[0].strip())):
        print("{t},\tThere is no new List...".format(t=datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        pass
    else:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        Vuln_extractor(soup, list_vuln)
        keys = Key_fetch()
        results_vuln = search(list_vuln, keys)
        Output_gerenator.out_gen(results_vuln,desc.split(":")[0].strip())
        Email_sender.send(desc)

if __name__ == "__main__":
    print("test")
    #schedule.every().day.do(Scheduled_task)
    schedule.every(1).minutes.do(Scheduled_task)
    while True:
        schedule.run_pending()