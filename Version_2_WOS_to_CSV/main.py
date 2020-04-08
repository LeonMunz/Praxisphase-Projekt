import bibtexparser
import glob
import os
import re
import csv
import pprint
from itertools import zip_longest
#--------------------------------------------------------------------------------------------------------------PARAMETER


Institution_Erstautor = 'radar'
Institution_Koautor = 'bonn'


#----------------------------------------------------------------------------------------------------------REGEX-PATTERN


Erstautoren_regex = re.compile(r'.*%s.*' % Institution_Erstautor, re.IGNORECASE)
Koautoren_regex = re.compile(r'.*\s\(Reprint\sAuthor\).*%s.*\.' % Institution_Koautor, re.IGNORECASE)


#-----------------------------------------------------------------------------------------------------MERGEN-DER-DATEIEN
path = ('./Dateien')
if os.path.exists(path) == True:
    print("BibTex Files aus ", path, "werden eingelesen.")
else:
    print(path, "existiert nicht.")


for filename in glob.glob(os.path.join(path, '*.bib')):
    print('Dateien werden zusammengeführt')
    with open(filename, 'r') as f:
        with open('./Zusammengeführte_BibTex_Files/collection.bib', 'a') as outfile:
            for line in f:
                outfile.write(line)

#------------------------------------------------------------------------------------------------PARSEN_DER_BIBTEX_FILES
with open('./Zusammengeführte_BibTex_Files/collection.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)

#--------------------------------------------------------------------------------------------ERSTAUTOREN-FILTER-FUNKTION
def Filtern_der_Autoren(a):
    print('Autoren werden gefiltert.')
    Autoren_Collection = []
    Autoren_Status = []
    for aut in a:
        oa = aut.get('oa')
        if oa is not None:                   #prüfen ob OA-Status vorhanden ist, wenn nein wird der Eintrag übersprungen
            add = aut.get('address')
            add2 = aut.get('affiliation')
            if Erstautoren_regex.match(add):
                if aut not in Autoren_Collection:                                                  #Doubletten Kontrolle
                    Autoren_Collection.append(aut)
                    Autoren_Status.append('Erstautor')
            if Koautoren_regex.match(add2):
                Autoren_Collection.append(aut)
                Autoren_Status.append('Reprint-Author')
    return Autoren_Collection, Autoren_Status

#-------------------------------------------------------------------------------------AKTIVIERUNG VON ERSTAUTOREN-FILTER
Autoren, Autoren_Status = Filtern_der_Autoren(bib_database.entries)
def Listen_Ranking(v):
    z = 0
    counter = []
    for x in v:
        x = v.count(v[z])
        z += 1
        counter.append(x)
        dictionary = dict(zip(v, counter))
    return(dictionary)
print('Gefundene Eintraege: ' + str(Listen_Ranking(Autoren_Status)))
#--------------------------------------------------------------------------------------------------------------OA-FILTER
def Filter_OA_Status(c):
    print('OA-Status wird gefiltert')
    oastatus = []
    for oa in c:
        add = oa.get('oa')
        q = add.replace('{', '')
        z = q.replace('}', '')
        oastatus.append(z)
    return oastatus
#-----------------------------------------------------------------------------------------------------------TITEL FILTER

def Collect_Titel(h):
    print('Titel werden gefiltert')
    Titel = []
    for tit in h:
        add = tit.get('title')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            y = z.replace('\n', '')
            Titel.append(y)
    return Titel
#--------------------------------------------------------------------------------------------------------ZEITRAUM FILTER

def Collect_Date(g):
    print('Datum wird gefiltert')
    Year = []
    Month = []
    for tim in g:
        year = tim.get('year')
        month = tim.get('month')
        if year is not None and month is not None:
            q = year.replace('{', '')
            z = q.replace('}', '')
            t = month.replace('{', '')
            v = t.replace('}', '')
            q = v.split(' ', 1)
            Year.append(z)
            Month.append(q[0])
    return Year, Month

Jahr, Monat = Collect_Date(Autoren)

#---------------------------------------------------------------------------------------------------------JOURNAL-FILTER

def Collect_Journal(d):
    print('Journal wird gefiltert')
    TempList = []
    for jour in d:
        add = jour.get('journal')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            TempList.append(z)
    return TempList
#---------------------------------------------------------------------------------------------------RESEARCH-AREA-FILTER

def Collect_Research_Areas(e):
    print('Research_Area wird gefiltert')
    re_area = []
    for ra in e:
        add=ra.get('research-areas')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            re_area.append(z)
    return re_area
#-------------------------------------------------------------------------------------------------------PUBLISHER-FILTER

def Collect_Publisher(f):
    print('Publisher wird gefiltert')
    PublisherTempList = []
    for pub in f:
        add=pub.get('publisher')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            PublisherTempList.append(z)
    return PublisherTempList
#------------------------------------------------------------------------------------------------FUNDING-ACKNOWLEDGEMENT

def Collect_FA(f):
    print('FA wird gefiltert')
    FA = []
    for dicti in f:
        add = dicti.get('funding-acknowledgement')
        if add is not None:
            a = add.replace('{', '')
            b = a.replace('}', '')
            c = b.replace('\n', '')
            d = c.replace('\\', '')
            FA.append(d)
    return FA
pprint.pprint(Collect_FA(Autoren))
#-----------------------------------------------------------------------------------------------------------AUTORENNAMEN

def Collect_Namen(g):
    print('Namen werden gefiltert')
    Namen = []
    for nam in g:
        add = nam.get('author')
        a = add.replace('{', '')
        b = a.replace('}', '')
        c = b.replace('and', '')
        d = c.replace('\n', '')
        Namen.append(d)
    return Namen
#-------------------------------------------------------------------------------------------------------------CSV-WRITER


attribute = [Collect_Titel(Autoren),
             Autoren_Status,
             Filter_OA_Status(Autoren),
             Jahr,
             Monat,
             Collect_Journal(Autoren),
             Collect_Research_Areas(Autoren),
             Collect_Publisher(Autoren),
             Collect_FA(Autoren),
             Collect_Namen(Autoren)]

export_data = zip_longest(*attribute, fillvalue='')

with open('numbers.csv', 'w', encoding="ISO-8859-1", newline='') as out:
      wr = csv.writer(out)
      wr.writerow(['Titel',
                   'Autoren_Status',
                   'OA_Status',
                   'Jahr',
                   'Monat',
                   'Journal',
                   'Disziplin',
                   'Publisher',
                   'Funding_Acknowledgement',
                   'Name'])
      wr.writerows(export_data)
out.close()




print(len(Collect_Titel(Autoren)))


os.remove('./Zusammengeführte_BibTex_Files/collection.bib')