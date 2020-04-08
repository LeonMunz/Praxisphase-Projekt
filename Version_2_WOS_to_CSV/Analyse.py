import pandas as pd
import pprint
import numpy as np
import matplotlib.pyplot as plt
import csv
from itertools import zip_longest

colnames = ['Titel',
              'Autor_Status',
              'OA_Status',
              'Jahr',
              'Monat',
              'Journal',
              'Disziplin',
              'Publisher',
              'Funding_Acknowledgement',
              'Name']

data = pd.read_csv('numbers.csv', names=colnames, skiprows=1)

df = pd.DataFrame(data)

dflist = [x for _, x in df.groupby('Autor_Status')]





def Listen_Ranking(v):
    z = 0
    counter = []
    for x in v:
        x = v.count(v[z])
        z += 1
        counter.append(x)
        dictionary = dict(zip(v, counter))
    return(dictionary)

#------------------------------------------------------------------------------------------------------------ERSTAUTOREN
titel = dflist[0].Titel.tolist()
autStatus = dflist[0].Autor_Status.tolist()
oaStatus = Listen_Ranking(dflist[0].OA_Status.tolist())
jahr = dflist[0].Jahr.tolist()
monat = dflist[0].Monat.tolist()
journal = Listen_Ranking(dflist[0].Journal.tolist())
disz = Listen_Ranking(dflist[0].Disziplin.tolist())
pub = Listen_Ranking(dflist[0].Publisher.tolist())
fa = Listen_Ranking(dflist[0].Funding_Acknowledgement.tolist())
autName = dflist[0].Name.tolist()
#--------------------------------------------------------------------------------------------------------------KOAUTOREN
ko_titel = dflist[1].Titel.tolist()
ko_autStatus = dflist[1].Autor_Status.tolist()
ko_oaStatus = Listen_Ranking(dflist[1].OA_Status.tolist())
ko_jahr = dflist[1].Jahr.tolist()
ko_monat = dflist[1].Monat.tolist()
ko_journal = Listen_Ranking(dflist[1].Journal.tolist())
ko_disz = Listen_Ranking(dflist[1].Disziplin.tolist())
ko_pub = Listen_Ranking(dflist[1].Publisher.tolist())
ko_fa =Listen_Ranking(dflist[1].Funding_Acknowledgement.tolist())
ko_autName = dflist[1].Name.tolist()
#-----------------------------------------------------------------------------------------------------------------------


def getlist(a):
    temp1 = []
    temp2 = []
    for key in a:
        temp1.append(key)
    for val in a.values():
        temp2.append(val)
    return temp1, temp2




attribute = [
             getlist(oaStatus)[0],
             getlist(oaStatus)[1],
             getlist(journal)[0],
             getlist(journal)[1],
             getlist(pub)[0],
             getlist(pub)[1],
             getlist(disz)[0],
             getlist(disz)[1]]
attributee = [
    getlist(ko_oaStatus)[0],
    getlist(ko_oaStatus)[1],
    getlist(ko_journal)[0],
    getlist(ko_journal)[1],
    getlist(ko_pub)[0],
    getlist(ko_pub)[1],
    getlist(ko_disz)[0],
    getlist(ko_disz)[1]]

export_data = zip_longest(*attribute, fillvalue='')
export_data2 = zip_longest(*attributee, fillvalue='')

with open('analyse.csv', 'w', encoding="ISO-8859-1", newline='') as out:
      wr = csv.writer(out)
      wr.writerow(['OA-Status Erstautoren',
                   'Anzahl',
                   'Journals',
                   'Anzahl',
                   'Publisher',
                   'Anzahl',
                   'Disziplin',
                   'Anzahl'])
      wr.writerows(export_data)
      wr.writerow(['OA-Status Koautoren',
                   'Anzahl',
                   'Journals',
                   'Anzahl',
                   'Publisher',
                   'Anzahl',
                   'Disziplin',
                   'Anzahl'])
      wr.writerows(export_data2)


out.close()




'''
height = getlist(oaStatus)[1]
bars = getlist(oaStatus)[0]
y_pos = np.arange(len(bars))
plt.bar(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
plt.xticks(y_pos, bars)
plt.show()
'''


















'''
print(len(titel))
print(len(autStatus))
print(len(oaStatus))
print(len(jahr))
print(len(monat))
print(len(journal))
print(len(disz))
print(len(pub))
print(len(fa))
print(len(autName))
'''