import bibtexparser
import glob
import os
import re
import pandas as pd

#--------------------------------------------------------------------------------------------------------------PARAMETER


Institution_Erstautor = 'radar'
Institution_Koautor = 'bonn'


#----------------------------------------------------------------------------------------------------------REGEX-PATTERN


Erstautoren_regex = re.compile(r'.*%s.*' % Institution_Erstautor, re.IGNORECASE)
Koautoren_regex = re.compile(r'.*\s\(Reprint\sAuthor\).*%s.*\.' % Institution_Koautor, re.IGNORECASE)


#-----------------------------------------------------------------------------------------------------MERGEN-DER-DATEIEN
path = ('./Dateien')
if os.path.exists(path) == True:
    print("BibTex Files aus ", path, "werden zusammengeführt.")
else:
    print(path, "existiert nicht.")


for filename in glob.glob(os.path.join(path, '*.bib')):
    with open(filename, 'r') as f:
        with open('./Zusammengeführte_BibTex_Files/collection.bib', 'a') as outfile:
            for line in f:
                outfile.write(line)

#------------------------------------------------------------------------------------------------PARSEN_DER_BIBTEX_FILES
with open('./Zusammengeführte_BibTex_Files/collection.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)

#--------------------------------------------------------------------------------------------ERSTAUTOREN-FILTER-FUNKTION
def Filtern_der_Erstautoren(a):
    Erstautoren_Collection = []
    for Erst in a:
        oa = Erst.get('oa')
        if oa is not None:   #prüfen ob OA-Status vorhanden ist, wenn nein wird der Eintrag übersprungen.
            add = Erst.get('address')
            if Erstautoren_regex.match(add):
                if dict not in Erstautoren_Collection:
                    Erstautoren_Collection.append(Erst)
    return Erstautoren_Collection
#-------------------------------------------------------------------------------------AKTIVIERUNG VON ERSTAUTOREN-FILTER
Erstautoren = Filtern_der_Erstautoren(bib_database.entries)
print('\n' + 'Erstautoren Einträge ' + str(len(Erstautoren)) + '\n')

#--------------------------------------------------------------------------------------------------------------OA-FILTER
def Filter_OA_Status(c):
    oastatus = []
    for oa in c:
        add = oa.get('oa')
        q = add.replace('{', '')
        z = q.replace('}', '')
        oastatus.append(z)
    return oastatus
#-----------------------------------------------------------------------------------------------------------TITEL FILTER

def Collect_Titel(h):
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
            Year.append(z)
            Month.append(v)
    for i in Year:
        zus = (zip(Year, Month))
    return list(zus)
#---------------------------------------------------------------------------------------------------------JOURNAL-FILTER

def Collect_Journal(d):
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
    FA = []
    for dicti in f:
        add = dicti.get('funding-acknowledgement')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            FA.append(z)
    return FA
#-------------------------------------------------------------------------------------------------------------CSV-WRITER

df = pd.DataFrame((list(zip(*[Collect_Titel(Erstautoren),
                              Filter_OA_Status(Erstautoren),
                              Collect_Date(Erstautoren),
                              Collect_Journal(Erstautoren),
                              Collect_Research_Areas(Erstautoren),
                              Collect_Publisher(Erstautoren),
                              Collect_FA(Erstautoren)]))))

df.columns = ['Titel', 'OA-Status', 'Datum', 'Journal', 'Disziplin', 'Publisher', 'Funding Acknowledgement']
df.to_csv('file.csv', index=False, header=True)





os.remove('./Zusammengeführte_BibTex_Files/collection.bib')