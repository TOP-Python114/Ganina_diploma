import os
import pandas as pd
import re
import requests
import sqlite3

number_of_pages = 50
data = []
job_title = ['Бухгалтер', 'Продавец', 'data science']
dfnew = pd.DataFrame(columns=['name', 'descr', 'alternate_url'])

for job in job_title:

    for i in range(number_of_pages):
        url = 'https://api.hh.ru/vacancies'
        par = {'text': job, 'area': '113', 'per_page': '10', 'page': i}
        req = requests.get(url, params=par)
        result = req.json()
        data.append(result)
        vacancy_details = data[0]['items'][0].keys()
        df = pd.DataFrame(columns=list(vacancy_details))
        ind = 0
        for k in range(len(data)):
            for j in range(len(data[k]['items'])):
                df.loc[ind] = data[k]['items'][j]
                ind += 1

        ind = 0
        for k in range(len(df)):
            dfnew.loc[ind] = df.loc[k]['name'], \
                             re.sub("{'requirement':|'responsibility':|}|<highlighttext>|</highlighttext>|'", "",
                                    str(df.loc[k]['snippet'])), df.loc[k]['alternate_url']
            ind += 1

if os.path.exists("vacancy.db"):
    os.remove("vacancy.db")

con = sqlite3.connect("vacancy.db")
dfnew.to_sql('vacancies', con)
