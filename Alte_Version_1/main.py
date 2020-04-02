import bibtexparser
import pprint
import glob
import os
import re
import time
import csv

#-----------------------NFO

'''
Damit alles funktioniert, bitte aus dem Repositorium die Ordner „Dateien“ und „Zusammengeführte_BibTex_Files“
in dasselbe Verzeichnis legen wie die „main.py“ Datei.

Im Ordner „Dateien“ liegt ein 500er Testset, es müssen also keine Daten händisch importiert werden.

Im Bereich „PARAMETER“ unter „Institution_Erstautor/ Koautor“ können beliebige Namen der Institutionen eingetragen
werden, nach diesen wird dann gesucht.
Die Ergebnismenge der einzelnen Suchanfragen hängt natürlich von dem 500er Testset ab.

Mit dem Parameter "CSV_Ergebnisliste" kann ein CSV-File innerhalb des Arbeitsverzeichnis mit den Ergebniswerten erstellt werden. (Wenn auf True)
Die Anderen Parameter sollten vorerst auf "True" bleiben, da diese ineinandergreifen und noch nicht optimiert wurden.
3

'''




#-----------------------PARAMETER

CSV_Ergebnisliste = False

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
#Ermöglicht eine Aufzählung der Funding-acknowledgements
Funding_Acknowledgement_Ertstautoren = True
Funding_Acknowledgement_Koautoren = True
#-----------------------REGEX-PATTERN4


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
    for Erst in a:
        add = Erst.get('address')
        if Erstautoren_regex.match(add):
            if dict not in Erstautoren_Collection:
                Erstautoren_Collection.append(Erst)
    return Erstautoren_Collection

#------AKTIVIEREN-DER-ERSTAUTOREN-FUNKTION

if Suche_nach_Erstautoren is True:
    Erstautoren = Filtern_der_Erstautoren(bib_database.entries)
    print('\n' + 'gefundene Erstautoren Einträge ' + str(len(Erstautoren)) + '\n')


#-----------------------KOAUTOREN-FILTER-FUNKTION


def Filtern_der_Koautoren(b):
    Koautoren_Collection = []
    for Ko in b:
        add = Ko.get('affiliation')
        if Koautoren_regex.match(add):
            if add not in Koautoren_Collection:
                Koautoren_Collection.append(Ko)
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

    for oa in c:
        add = oa.get('oa')
        if add is not None:
            if oa_other_GoldRegex.match(add):
                if oa not in OA_Other_Gold:
                    OA_Other_Gold.append(oa)
            if oa_doaj_GoldRegex.match(add):
                if oa not in OA_Doaj_Gold:
                    OA_Doaj_Gold.append(oa)
            if oa_Green_published.match(add):
                if oa not in OA_Green_Published:
                    OA_Green_Published.append(oa)
            if oa_Green_accepted.match(add):
                if oa not in OA_Green_Published:
                    OA_Green_Published.append(oa)
            if oa_Bronze_regex.match(add):
                if oa not in OA_Bronze:
                    OA_Bronze.append(oa)
            else:
                if oa not in OA_Other:
                    OA_Other.append(oa)
    return OA_Other_Gold,\
           OA_Doaj_Gold,\
           OA_Green_Published,\
           OA_Bronze,\
           OA_Other


#-------AKTIVIEREN DER OA-FILTER-FUNKTION

if OA_Status_Erstautoren is True:
    OA_OtherGold_Erstautoren,\
    OA_DoajGold_Erstautoren,\
    OA_GreenPublished_Erstautoren,\
    OA_Bronze_Erstautoren,\
    OA_Other_Erstautoren\
        = Filter_OA_Status(Erstautoren)


if OA_Status_Koautoren is True:
    OA_OtherGold_Koautoren,\
    OA_DoajGold_Koautoren,\
    OA_GreenPublished_Koautoren,\
    OA_Bronze_Koautoren,\
    OA_Other_Koautoren\
        = Filter_OA_Status(Koautoren)

#----------------------FILTER-NACH-JOURNAL


def Collect_Journal(d):
    TempList = []
    for jour in d:
        add = jour.get('journal')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            TempList.append(z)
            p = Listen_Ranking(TempList)
    return p

if Journal_Analyse_Erstautoren is True:
    Journal_Erstautoren = [Collect_Journal(OA_OtherGold_Erstautoren),
                           Collect_Journal(OA_DoajGold_Erstautoren),
                           Collect_Journal(OA_GreenPublished_Erstautoren),
                           Collect_Journal(OA_Bronze_Erstautoren),
                           Collect_Journal(OA_Other_Erstautoren)]


if Journal_Analyse_Koautoren is True:
    Journal_Koautoren = [Collect_Journal(OA_OtherGold_Koautoren),
                         Collect_Journal(OA_DoajGold_Koautoren),
                         Collect_Journal(OA_GreenPublished_Koautoren),
                         Collect_Journal(OA_Bronze_Koautoren),
                         Collect_Journal(OA_Other_Koautoren)]



#---------------------FILTERN NACH DISZIPLIN


def Collect_Research_Areas(e):
    DisziplinenTempList = []
    for dis in e:
        add = dis.get('research-areas')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            DisziplinenTempList.append(z)
            x=Listen_Ranking(DisziplinenTempList)
    return x

if Disziplinen_Analyse_Erstautoren is True:
    Disziplin_Erstautoren = [Collect_Research_Areas(OA_OtherGold_Erstautoren),
                             Collect_Research_Areas(OA_DoajGold_Erstautoren),
                             Collect_Research_Areas(OA_GreenPublished_Erstautoren),
                             Collect_Research_Areas(OA_Bronze_Erstautoren),
                             Collect_Research_Areas(OA_Other_Erstautoren)]


if Disziplinen_Analyse_Koautoren is True:
    Disziplin_Koautoren = [Collect_Research_Areas(OA_OtherGold_Koautoren),
                           Collect_Research_Areas(OA_DoajGold_Koautoren),
                           Collect_Research_Areas(OA_GreenPublished_Koautoren),
                           Collect_Research_Areas(OA_Bronze_Koautoren),
                           Collect_Research_Areas(OA_Other_Koautoren)]


#---------------------FILTERN NACH PUBLISHER


def Collect_Publisher(f):
    PublisherTempList = []
    for pub in f:
        add=pub.get('publisher')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            PublisherTempList.append(z)
            x=Listen_Ranking(PublisherTempList)
    return x

if Publisher_Analyse_Erstautoren is True:
    Publisher_Erstautoren = [Collect_Publisher(OA_OtherGold_Erstautoren),
                             Collect_Publisher(OA_DoajGold_Erstautoren),
                             Collect_Publisher(OA_GreenPublished_Erstautoren),
                             Collect_Publisher(OA_Bronze_Erstautoren),
                             Collect_Publisher(OA_Other_Erstautoren)]


if Publisher_Analyse_Koautoren is True:
    Publisher_Koautoren = [Collect_Publisher(OA_OtherGold_Koautoren),
                           Collect_Publisher(OA_DoajGold_Koautoren),
                           Collect_Publisher(OA_GreenPublished_Koautoren),
                           Collect_Publisher(OA_Bronze_Koautoren),
                           Collect_Publisher(OA_Other_Koautoren)]


#---------------------FILTERN NACH JAHR


def Collect_Years(g):
    Year = []
    Month = []
    for tim in g:
        year = tim.get('year')
        month = tim.get('month')
        if year is not None and month is not None:
            q = year.replace('{', '')
            z = q.replace('}', '')
            t = month.replace('{', '')
            v = q.replace('}', '')
            Year.append(z)
            Month.append(v)
    b = Listen_Ranking(z)
    return b

#Funktioniert noch nicht

#---------------------FILTERN NACH FOUNDING ACKNOLEDGEMENT


def Collect_FA(f):
    FA = []
    for dicti in f:
        add = dicti.get('funding-acknowledgement')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            FA.append(z)
            a = Listen_Ranking(FA)
    return a

#---------------------FILTERN DER TITEL

def Collect_Titel(h):
    Titel = []
    for tit in h:
        add = tit.get('title')
        if add is not None:
            q = add.replace('{', '')
            z = q.replace('}', '')
            Titel.append(z)
    return Titel


if Funding_Acknowledgement_Ertstautoren is True:
    Funding_Erstautoren = [Collect_FA(OA_OtherGold_Erstautoren),
                            Collect_FA(OA_DoajGold_Erstautoren),
                            Collect_FA(OA_GreenPublished_Erstautoren),
                            Collect_FA(OA_Bronze_Erstautoren),
                            Collect_FA(OA_OtherGold_Erstautoren)]

if Funding_Acknowledgement_Koautoren is True:
    Funding_Koautoren = [Collect_FA(OA_OtherGold_Koautoren),
                          Collect_FA(OA_DoajGold_Koautoren),
                          Collect_FA(OA_GreenPublished_Koautoren),
                          Collect_FA(OA_Bronze_Koautoren),
                          Collect_FA(OA_OtherGold_Koautoren)]



#------Prints
print(len(Collect_Titel(Erstautoren)))


print('OA-Status der Erstautoren der Institution: ' + Institution_Erstautor)
print('OA Other Gold Erstautoren ' + str(len(OA_OtherGold_Erstautoren)))
print('Journals: ' + str(Journal_Erstautoren[0]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[0]))
print('Publisher: ' + str(Publisher_Erstautoren[0]))
print('Funding: ' + str(Funding_Erstautoren[0]))

print('OA DOAJ GOLD Erstautoren ' + str(len(OA_DoajGold_Erstautoren)))
print('Journals: ' + str(Journal_Erstautoren[1]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[1]))
print('Publisher: ' + str(Publisher_Erstautoren[1]))
print('Funding: ' + str(Funding_Erstautoren[1]))

print('OA GreenPublished Erstautoren ' + str(len(OA_GreenPublished_Erstautoren)))
print('Journals: ' + str(Journal_Erstautoren[2]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[2]))
print('Publisher: ' + str(Publisher_Erstautoren[2]))
print('Funding: ' + str(Funding_Erstautoren[2]))

print('OA Bronze Erstautoren ' + str(len(OA_Bronze_Erstautoren)))
print('Journals: ' + str(Journal_Erstautoren[3]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[3]))
print('Publisher: ' + str(Publisher_Erstautoren[3]))
print('Funding: ' + str(Funding_Erstautoren[3]))

print('OA Other Erstautoren ' + str(len(OA_Other_Erstautoren)))
print('Journals: ' + str(Journal_Erstautoren[4]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[4]))
print('Publisher: ' + str(Publisher_Erstautoren[4]))
print('Funding: ' + str(Funding_Erstautoren[4]) + '\n')

print('Koautoren der Institution: ' + Institution_Koautor)

print('OA-Status der Koautoren: ')
print('OA Other Gold Koautoren ' + str(len(OA_OtherGold_Koautoren)))
print('Journals: ' + str(Journal_Erstautoren[0]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[0]))
print('Publisher: ' + str(Publisher_Erstautoren[0]))
print('Funding: ' + str(Funding_Koautoren[0]))


print('OA DOAJ GOLD Koautoren ' + str(len(OA_DoajGold_Koautoren)))
print('Journals: ' + str(Journal_Erstautoren[1]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[1]))
print('Publisher: ' + str(Publisher_Erstautoren[1]))
print('Funding: ' + str(Funding_Koautoren[1]))

print('OA GreenPublished Koautoren ' + str(len(OA_GreenPublished_Koautoren)))
print('Journals: ' + str(Journal_Erstautoren[2]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[2]))
print('Publisher: ' + str(Publisher_Erstautoren[2]))
print('Founding: ' + str(Funding_Koautoren[2]))

print('OA Bronze Koautoren ' + str(len(OA_Bronze_Koautoren)))
print('Journals: ' + str(Journal_Erstautoren[3]))
print('Disziplinen: ' + str(Disziplin_Erstautoren[3]))
print('Publisher: ' + str(Publisher_Erstautoren[3]))
print('Funding: ' + str(Funding_Koautoren[3]))

print('OA Other Koautoren ' + str(len(OA_Other_Koautoren)))
print('Journals: ' + str(str(Journal_Erstautoren[4])))
print('Disziplinen: ' + str(Disziplin_Erstautoren[4]))
print('Publisher: ' + str(Publisher_Erstautoren[4]))
print('Funding: ' + str(Funding_Koautoren[4]))

os.remove('./Zusammengeführte_BibTex_Files/collection.bib')