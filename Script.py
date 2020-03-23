#-----------------------IMPORT-----------------------#
import bibtexparser
import pprint
import glob
import os
import re
import time

'''
WICHTIG:

Dieses Script bildet nur die Basis des Tools, auf welcher weitere Features implementiert werden, teilweise funktionieren diese
noch nicht im ganzen, daher hier nur das Grundgerüst.

Damit das tool funktioniert müssen im Verzeichnis die Ordner "Dateien" und "Zusammengeführte_BibTex_Files" existieren.
In ersteren kommen alle geladenen BibTex-Files, zweiterer bleibt leer, hier wird das aus den einzelnen Files
zusammengeführte Dokument temporär zwischengelagert (Das zusammengeführte File wird nach ausführen des Scripts wieder gelöscht).

Unter "Parameter" -> "Institution" lässt sich die zu suchende Institution eintragen, dies kann auch eine beliebige Textzeile aus
dem Feld "Address" im BibTex-File sein. Die Variable "Institution" ersetzt nur den Teil im Regex-Pattern.


Die print Optionen welche momentan voreingestellt sind liefern einen Überblick über die relevanten Fragestellungen, inklusive
zweier ausführlicher Dicts welche die Namen der Journals und deren Häufigkeit, sowie die Disziplinen und deren Häufigkeit 
aufzeigen.

'''





#-----------------------PARAMETER

Institution = 'radar'




#-----------------------REGEX-PATTERN


regex = re.compile(r'.*%s.*' % Institution,re.IGNORECASE)
oaGoldRegex = re.compile(r'.*Gold.*', re.IGNORECASE)
oaGreenRegex = re.compile(r'.*Green.*', re.IGNORECASE)



#-----------------------GLOBALE-VARIABLEN


Erstautoren=[]
Koautoren=[]

JournalCount=[]

OA_GoldCount=[]
Disziplinen_OA_Gold=[]
OA_GreenCount=[]
Disziplinen_OA_Green=[]
OA_BothCount=[]
OA_Other=[]
Disziplinen_OA_Other=[]

AutorenNamen = []
KoautorenNamen=[]
Disziplinen = []
Journals=[]


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


#-----------------------ERSTAUTOREN-FILTER


def Filtern_der_Erstautoren():
    for dict in bib_database.entries:
        add=dict.get('address')
        if regex.match(add):
            if dict not in Erstautoren:
                Erstautoren.append(dict)
                for nam in Erstautoren:
                    x=nam.get('author')
                    y=x.replace('and', '')
                    z=y.replace('\n', '')
                    AutorenNamen.append(z)

#-----------------------KOAUTOREN-FILTER


def Filtern_der_Koautoren():
    for dict in bib_database.entries:
        add=dict.get('affiliation')
        if regex.match(add):
            if dict not in Koautoren:
                Koautoren.append(dict)
                for nam in Erstautoren:
                    x=nam.get('author')
                    y=x.replace('and', '')
                    z=y.replace('\n', '')
                    KoautorenNamen.append(z)


#-----------------------OA-STATUS-FILTER


def Filter_OA_Status():
    for dict in Erstautoren:
        add=dict.get('oa')
        if add is not None:
            if oaGoldRegex.match(add):
                if dict not in OA_GoldCount:
                    OA_GoldCount.append(dict)
                    for dis in OA_GoldCount:
                        if dis is not None:
                            disTemp=dis.get('research-areas')
                            Disziplinen_OA_Gold.append(disTemp)
            if oaGreenRegex.match(add):
                if dict not in OA_GreenCount:
                    OA_GreenCount.append(dict)
                    for dis in OA_GreenCount:
                        if dis is not None:
                            disTemp2=dis.get('research-areas')
                            Disziplinen_OA_Green.append(disTemp2)
            else:
                OA_Other.append(dict)
                for other in OA_Other:
                    if other is not None:
                        disTemp3 = other.get('research-areas')
                        Disziplinen_OA_Other.append(disTemp3)



#----------------------FILTER-NACH-JOURNAL


def Collect_Journal():
    for dict in Erstautoren:
        add=dict.get('journal')
        if add is not None:
            Journals.append(add)


#---------------------FILTERN NACH DISZIPLIN


def Collect_Research_Areas():
    for dict in Erstautoren:
        add=dict.get('research-areas')
        if add is not None:
            Disziplinen.append(add)


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


#-----------------------AUFRUFEN DER FUNKTIONEN




Filtern_der_Erstautoren()
Filter_OA_Status()
Filtern_der_Koautoren()
Collect_Journal()
Collect_Research_Areas()

Listen_Ranking(Journals)
Listen_Ranking(Disziplinen)




#-------------------HÄUFIGKEITS-VARIABLEN
Häufigkeit_Journals=Listen_Ranking(Journals)
Häufigkeit_Disziplinen=Listen_Ranking(Disziplinen)

#research-areas




pprint.pprint(Häufigkeit_Journals)
pprint.pprint(Häufigkeit_Disziplinen)
#pprint.pprint(Disziplinen)
#pprint.pprint(Disziplinen_OA_Other)
#pprint.pprint(Disziplinen_OA_Gold)
#pprint.pprint(Disziplinen_OA_Green)
#pprint.pprint(Erstautoren)
print ('Erstautoren ' + str((len(Erstautoren))))
print ('Koautoren ' + str((len(Koautoren))))
print ('OA-Gold ' + str((len(OA_GoldCount))))
print ('OA-Green ' + str((len(OA_GreenCount))))
print('OA-Other '+ str((len(OA_Other))))
print('Journals '+ str((len(Journals))))
#print(AutorenNamen)


os.remove('./Zusammengeführte_BibTex_Files/collection.bib')