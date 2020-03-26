import bibtexparser
import pprint
import glob
import os
import re
import time
#-----------------------PARAMETER

Institution_Erstautor = 'radar'
Institution_Koautor = 'bonn'

Suche_nach_Erstautoren = True
Suche_nach_Koautoren = True

OA_Status_Erstautoren = True
OA_Status_Koautoren = True

#Ermöglicht eine Aufzählung welche Journals in einem OA-Status vorkommen und wie oft
Journal_Analyse_Erstautoren = True
Journal_Analyse_Koautoren = True
#Ermöglicht eine Aufzählung welche Disziplinen vorkommen und wie oft
Disziplinen_Analyse_Erstautoren = True
Disziplinen_Analyse_Koautoren = True
#Ermöglicht eine Aufzählung welche Publisher vorkommen und wie oft
Publisher_Analyse_Erstautoren = True
Publisher_Analyse_Koautoren = True
#Ermöglicht eine Aufzählung der Jahre und deren Häufigkeit
Jahr_Analyse_Erstautoren = True
Jahr_Analyse_Koautoren = True

#-----------------------REGEX-PATTERN


Erstautoren_regex = re.compile(r'.*%s.*' % Institution_Erstautor, re.IGNORECASE)
Koautoren_regex = re.compile(r'.*\s\(Reprint\sAuthor\).*%s.*\.' % Institution_Koautor, re.IGNORECASE)

oa_other_GoldRegex = re.compile(r'.*Other\sGold.*', re.IGNORECASE)
oa_doaj_GoldRegex = re.compile(r'.*DOAJ\sGold.*', re.IGNORECASE)
oa_Green_accepted = re.compile(r'.*.*Green\sAccepted.*.*', re.IGNORECASE)
oa_Green_published = re.compile(r'.*.*Green\sPublished.*.*', re.IGNORECASE)
oa_Bronze_regex = re.compile(r'.*.*Bronze.*.*', re.IGNORECASE)


#-----------------------MERGEN-DER-DATEIEN


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


#-----------------------PARSEN_DER_BIBTEX_FILES


with open('./Zusammengeführte_BibTex_Files/collection.bib') as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)

#---------------------LISTEN-RANKING-FUNKTION
""""
Die Funktion 'Listen_Ranking' erstellt ein Dictionary aus den Werten einer Liste,
zählt die Häufigkeit dieser und gibt diese als 'Value' im Dictionary wieder.

Die Variable welche die zu verarbeitende Liste enthält wird dem Funktionsaufruf 
übergeben.

"""

def Listen_Ranking(v):
    z = 0
    counter = []
    for x in v:
        x = v.count(v[z])
        z += 1
        counter.append(x)
        dictionary = dict(zip(v, counter))
    return(dictionary)
#-----------------------ERSTAUTOREN-FILTER-FUNKTION


def Filtern_der_Erstautoren(a):
    Erstautoren_Collection = []
    for dict in a:
        add=dict.get('address')
        if Erstautoren_regex.match(add):
            if dict not in Erstautoren_Collection:
                Erstautoren_Collection.append(dict)
    return Erstautoren_Collection

#------AKTIVIEREN-DER-ERSTAUTOREN-FUNKTION

if Suche_nach_Erstautoren is True:
    Erstautoren = Filtern_der_Erstautoren(bib_database.entries)
    print('\n' + 'gefundene Erstautoren Einträge ' + str(len(Erstautoren)) + '\n')


#-----------------------KOAUTOREN-FILTER-FUNKTION


def Filtern_der_Koautoren(b):
    Koautoren_Collection = []
    for dict in b:
        add=dict.get('affiliation')
        if Koautoren_regex.match(add):
            if dict not in Koautoren_Collection:
                Koautoren_Collection.append(dict)
    return Koautoren_Collection

#------AKTIVIEREN-DER-KOAUTOREN-FUNKTION

if Suche_nach_Koautoren is True:
    Koautoren  = Filtern_der_Koautoren(bib_database.entries)
    print('\n' + 'gefundene Koautoren Einträge ' + str(len(Koautoren)) + '\n')

#-----------------------OA-STATUS-FILTER
'''
PROBLEM: Momentan landen Mehrfachzuweisungen von OA Status in OA_Other, zeichnet ungenaues Bild, 
die meisten Fälle weisen eine Zuweisung von "{DOAJ Gold, Green Accepted, Green Published}" aber auch "{Other Gold}" 
und "{DOAJ Gold}"auf.
'''

def Filter_OA_Status(c):
    OA_Other_Gold = []
    OA_Doaj_Gold = []
    OA_Green_Published = []
    OA_Bronze = []
    OA_Other =[]

    for dict in c:
        add=dict.get('oa')
        if add is not None:
            if oa_other_GoldRegex.match(add):
                if dict not in OA_Other_Gold:
                    OA_Other_Gold.append(dict)
            if oa_doaj_GoldRegex.match(add):
                if dict not in OA_Doaj_Gold:
                    OA_Doaj_Gold.append(dict)
            if oa_Green_published.match(add):
                if dict not in OA_Green_Published:
                    OA_Green_Published.append(dict)
            if oa_Green_accepted.match(add):
                if dict not in OA_Green_Published:
                    OA_Green_Published.append(dict)
            if oa_Bronze_regex.match(add):
                if dict not in OA_Bronze:
                    OA_Bronze.append(dict)
            else:
                if dict not in OA_Other:
                    OA_Other.append(dict)
    return OA_Other_Gold, OA_Doaj_Gold, OA_Green_Published, OA_Bronze, OA_Other


#-------AKTIVIEREN DER OA-FILTER-FUNKTION

if OA_Status_Erstautoren is True:
    OA_OtherGold_Erstautoren, OA_DoajGold_Erstautoren, OA_GreenPublished_Erstautoren, OA_Bronze_Erstautoren, OA_Other_Erstautoren = Filter_OA_Status(Erstautoren)


if OA_Status_Koautoren is True:
    OA_OtherGold_Koautoren, OA_DoajGold_Koautoren, OA_GreenPublished_Koautoren, OA_Bronze_Koautoren, OA_Other_Koautoren = Filter_OA_Status(Koautoren)

#----------------------FILTER-NACH-JOURNAL


def Collect_Journal(d):
    TempList = []
    for dict in d:
        add=dict.get('journal')
        if add is not None:
            TempList.append(add)
            x=Listen_Ranking(TempList)
    return x

if Journal_Analyse_Erstautoren is True:
    Journal_Other_Gold_Erstautoren = Collect_Journal(OA_OtherGold_Erstautoren)
    Journal_Doaj_Gold_Erstautoren = Collect_Journal(OA_DoajGold_Erstautoren)
    Journal_Green_Published_Erstautoren = Collect_Journal(OA_GreenPublished_Erstautoren)
    Journal_Bronze_Erstautoren = Collect_Journal(OA_Bronze_Erstautoren)
    Journal_Other_Erstautoren = Collect_Journal(OA_Other_Erstautoren)

if Journal_Analyse_Koautoren is True:
    Journal_Other_Gold_Koautoren = Collect_Journal(OA_OtherGold_Koautoren)
    Journal_Doaj_Gold_Koautoren = Collect_Journal(OA_DoajGold_Koautoren)
    Journal_Green_Published_Koautoren = Collect_Journal(OA_GreenPublished_Koautoren)
    Journal_Bronze_Koautoren = Collect_Journal(OA_Bronze_Koautoren)
    Journal_Other_Koautoren = Collect_Journal(OA_Other_Koautoren)


#---------------------FILTERN NACH DISZIPLIN


def Collect_Research_Areas(e):
    DisziplinenTempList = []
    for dict in e:
        add=dict.get('research-areas')
        if add is not None:
            DisziplinenTempList.append(add)
            x=Listen_Ranking(DisziplinenTempList)
    return x

if Disziplinen_Analyse_Erstautoren is True:
    Disziplin_Other_Gold_Erstautoren = Collect_Research_Areas(OA_OtherGold_Erstautoren)
    Disziplin_Doaj_Gold_Erstautoren = Collect_Research_Areas(OA_DoajGold_Erstautoren)
    Disziplin_Green_Published_Erstautoren = Collect_Research_Areas(OA_GreenPublished_Erstautoren)
    Disziplin_Bronze_Erstautoren = Collect_Research_Areas(OA_Bronze_Erstautoren)
    Disziplin_Other_Erstautoren = Collect_Research_Areas(OA_Other_Erstautoren)

if Disziplinen_Analyse_Koautoren is True:
    Disziplin_Other_Gold_Koautoren = Collect_Research_Areas(OA_OtherGold_Koautoren)
    Disziplin_Doaj_Gold_Koautoren = Collect_Research_Areas(OA_DoajGold_Koautoren)
    Disziplin_Green_Published_Koautoren = Collect_Research_Areas(OA_GreenPublished_Koautoren)
    Disziplin_Bronze_Koautoren = Collect_Research_Areas(OA_Bronze_Koautoren)
    Disziplin_Other_Koautoren = Collect_Research_Areas(OA_Other_Koautoren)

#---------------------FILTERN NACH PUBLISHER


def Collect_Publisher(f):
    PublisherTempList = []
    for dict in f:
        add=dict.get('publisher')
        if add is not None:
            PublisherTempList.append(add)
            x=Listen_Ranking(PublisherTempList)
    return x

#---------------------FILTERN NACH JAHR


def Collect_Years(g):
    YearTempList = []
    for dict in g:
        add=dict.get('year')
        if add is not None:
            YearTempList.append(add)
            x=Listen_Ranking(YearTempList)
    return x

print(Collect_Years(Koautoren))

if Publisher_Analyse_Erstautoren is True:
    Publisher_Other_Gold_Erstautoren = Collect_Publisher(OA_OtherGold_Erstautoren)
    Publisher_Doaj_Gold_Erstautoren = Collect_Publisher(OA_DoajGold_Erstautoren)
    Publisher_Green_Published_Erstautoren = Collect_Publisher(OA_GreenPublished_Erstautoren)
    Publisher_Bronze_Erstautoren = Collect_Publisher(OA_Bronze_Erstautoren)
    Publisher_Other_Erstautoren = Collect_Publisher(OA_Other_Erstautoren)

if Publisher_Analyse_Koautoren is True:
    Publisher_Other_Gold_Koautoren = Collect_Publisher(OA_OtherGold_Koautoren)
    Publisher_Doaj_Gold_Koautoren = Collect_Publisher(OA_DoajGold_Koautoren)
    Publisher_Green_Published_Koautoren = Collect_Publisher(OA_GreenPublished_Koautoren)
    Publisher_Bronze_Koautoren = Collect_Publisher(OA_Bronze_Koautoren)
    Publisher_Other_Koautoren = Collect_Publisher(OA_Other_Koautoren)


#------Prints
'''
#pprint.pprint(OA_GreenPublished_Koautoren)
print('OA-Status der Erstautoren: ')
print('OA Other Gold Erstautoren ' + str(len(OA_OtherGold_Erstautoren)))
print('Journals: ' + str(Journal_Other_Gold_Erstautoren))
print('Disziplinen: ' + str(Disziplin_Other_Gold_Erstautoren))
print('Publisher: ' + str(Publisher_Other_Gold_Erstautoren))

print('OA DOAJ GOLD Erstautoren ' + str(len(OA_DoajGold_Erstautoren)))
print('Journals: ' + str(Journal_Doaj_Gold_Erstautoren))
print('Disziplinen: ' + str(Disziplin_Doaj_Gold_Erstautoren))
print('Publisher: ' + str(Publisher_Doaj_Gold_Erstautoren))

print('OA GreenPublished Erstautoren ' + str(len(OA_GreenPublished_Erstautoren)))
print('Journals: ' + str(Journal_Green_Published_Erstautoren))
print('Disziplinen: ' + str(Disziplin_Green_Published_Erstautoren))
print('Publisher: ' + str(Publisher_Green_Published_Erstautoren))

print('OA Bronze Erstautoren ' + str(len(OA_Bronze_Erstautoren)))
print('Journals: ' + str(Journal_Bronze_Erstautoren))
print('Disziplinen: ' + str(Disziplin_Bronze_Erstautoren))
print('Publisher: ' + str(Publisher_Bronze_Erstautoren))

print('OA Other Erstautoren ' + str(len(OA_Other_Erstautoren)))
print('Journals: ' + str(Journal_Other_Erstautoren))
print('Disziplinen: ' + str(Disziplin_Other_Erstautoren))
print('Publisher: ' + str(Publisher_Other_Erstautoren) + '\n')

print('Koautoren: ')

print('OA-Status der Koautoren: ')
print('OA Other Gold Koautoren ' + str(len(OA_OtherGold_Koautoren)))
print('Journals: ' + str(Journal_Other_Gold_Koautoren))
print('Disziplinen: ' + str(Disziplin_Other_Gold_Koautoren))
print('Publisher: ' + str(Publisher_Other_Gold_Koautoren))


print('OA DOAJ GOLD Koautoren ' + str(len(OA_DoajGold_Koautoren)))
print('Journals: ' + str(Journal_Doaj_Gold_Koautoren))
print('Disziplinen: ' + str(Disziplin_Doaj_Gold_Koautoren))
print('Publisher: ' + str(Publisher_Doaj_Gold_Koautoren))

print('OA GreenPublished Koautoren ' + str(len(OA_GreenPublished_Koautoren)))
print('Journals: ' + str(Journal_Green_Published_Koautoren))
print('Disziplinen: ' + str(Disziplin_Green_Published_Koautoren))
print('Publisher: ' + str(Publisher_Green_Published_Koautoren))


print('OA Bronze Koautoren ' + str(len(OA_Bronze_Koautoren)))
print('Journals: ' + str(Journal_Bronze_Koautoren))
print('Disziplinen: ' + str(Disziplin_Bronze_Koautoren))
print('Publisher: ' + str(Publisher_Bronze_Erstautoren))

print('OA Other Koautoren ' + str(len(OA_Other_Koautoren)))
print('Journals: ' + str(str(Journal_Other_Koautoren)))
print('Disziplinen: ' + str(Disziplin_Other_Koautoren))
print('Publisher: ' + str(Publisher_Other_Erstautoren))
'''
os.remove('./Zusammengeführte_BibTex_Files/collection.bib')