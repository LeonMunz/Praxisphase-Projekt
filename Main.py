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
    print('gefundene erstautoren Einträge ' + str(len(Erstautoren)) + '\n')


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
    Kotautoren = Filtern_der_Koautoren(bib_database.entries)



#-----------------------OA-STATUS-FILTER
'''
PROBLEM: Momentan landen Mehrfachzuweiseungen von OA Status in OA_Other, zeichnet ungenaues Bild 
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

a,b,c,d,e = Filter_OA_Status(Erstautoren)


if OA_Status_Erstautoren is True:
    OA_OtherGold_Erstautoren, OA_DoajGold_Erstautoren, OA_GreenPublished_Erstautoren, OA_Bronze_Erstautoren, OA_Other_Erstautoren = Filter_OA_Status(Erstautoren)

if OA_Status_Koautoren is True:
    OA_OtherGold_Koautoren, OA_DoajGold_Koautoren, OA_GreenPublished_Koautoren, OA_Bronze_Koautoren, OA_Other_Koautoren = Filter_OA_Status(Kotautoren)




#------Prints

#pprint.pprint(OA_GreenPublished_Koautoren)
print('OA-Status der Erstautoren: ')
print('Other Gold Erstautoren ' + str(len(OA_OtherGold_Erstautoren)))
print('DOAJ GOLD Erstautoren ' + str(len(OA_DoajGold_Erstautoren)))
print('GreenPublished Erstautoren ' + str(len(OA_GreenPublished_Erstautoren)))
print('Bronze Erstautoren ' + str(len(OA_Bronze_Erstautoren)))
print('Other Erstautoren ' + str(len(OA_Other_Erstautoren)) + '\n')
print('OA-Status der Koautoren: ')
print('Other Gold Koautoren ' + str(len(OA_OtherGold_Koautoren)))
print('DOAJ GOLD Koautoren ' + str(len(OA_DoajGold_Koautoren)))
print('GreenPublished Koautoren ' + str(len(OA_GreenPublished_Koautoren)))
print('Bronze Koautoren ' + str(len(OA_Bronze_Koautoren)))
print('Other Koautoren ' + str(len(OA_Other_Koautoren)))

os.remove('./Zusammengeführte_BibTex_Files/collection.bib')