import bibtexparser
import glob
import os
from os import path
import re
import csv
import pprint
from itertools import zip_longest
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
import pandas as pd
import pprint
import numpy as np
import matplotlib.pyplot as plt
import csv
from itertools import zip_longest

#-----------------------------------------------------------------------------------------------------------------------
'''
Innheralb des ersten Teils des Scripts werden Funktionen definiert.
Im zweiten Teil wird die Grafische Oberfläche definiert

'''




#----------------------------------------------------------------------------------------------------AUSWAHL-DES-ORDNERS
'''
Die Funktion "selectDir" ermöglicht das Festlegen, via grafischer Oberfläche, eines Speicherorts der zu analysierenden
BibTex-Files.
'''

def selectDir():
    sdir = filedialog.askdirectory()
    ausbtn.configure(text=sdir)
    for filename in glob.glob(os.path.join(sdir, '*.bib')):
        print('Dateien werden zusammengeführt')
        with open(filename, 'r') as f:
            with open('./Zusammengeführte_BibTex_Files/collection.bib', 'a') as outfile:
                for line in f:
                    outfile.write(line)
#---------------------------------------------------------------------------------------EINGABE-DER-SUCHPARAMETER-IN-GUI
'''
Die Funktion "sb" (search bar) ermöglicht die eingabe der Suchparameter via grafischer Oberfläche
'''
def sb():
    if EASB.get():
        ea = EASB.get()
        EAanzeige.configure(text=ea, fg='green')
    else:
        EAanzeige.configure(text='Eine Eingabe beider Felder wird benötigt', anchor='e', fg='red')
    if KASB.get():
        ka = KASB.get()
        KAanzeige.configure(text=ka, fg='green')
    else:
        KAanzeige.configure(text='Eine Eingabe beider Felder wird benötigt', anchor='e', fg='red')
    return ea, ka
#--------------------------------------------------------------------------------------------------AUSFÜHREN DES SCRIPTS
def start():
    with open('./Zusammengeführte_BibTex_Files/collection.bib') as bibtex_file:
        bibtex_str = bibtex_file.read()
    bib_database = bibtexparser.loads(bibtex_str)
    ea = sb()[0]
    ka = sb()[1]
    Autoren, Autoren_Status = Filtern_der_Autoren(bib_database.entries)
    Jahr, Monat = Collect_Date(Autoren)
    #-------------------------------------------------------------------------------------SCHREIBEN DES RAW-RESULT-FILES
    attribute = [Collect_Titel(Autoren),
                 Autoren_Status,
                 Filter_OA_Status(Autoren),
                 Jahr,
                 MonthtoNumber(Monat),
                 Collect_Journal(Autoren),
                 Collect_Research_Areas(Autoren),
                 Collect_Publisher(Autoren),
                 Collect_FA(Autoren),
                 Collect_Namen(Autoren)]
    export_data = zip_longest(*attribute, fillvalue='')
    with open('resultfromGUI.csv', 'w', encoding="ISO-8859-1", newline='') as out:
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
        os.remove('./Zusammengeführte_BibTex_Files/collection.bib')
    out.close()
    # -----------------------------------EINLESEN_DES_RAW-RESULT-FILES_ALS_PANDAS_DATAFRAME_UM_ANALYSE-FILE_ZU_ERSTELLEN
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
    data = pd.read_csv('resultfromGUI.csv', names=colnames, skiprows=1)
    df = pd.DataFrame(data)
    dflist = [x for _, x in df.groupby('Autor_Status')]
    # -------------------------------------------------------------------------------------------------------ERSTAUTOREN
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
    # ---------------------------------------------------------------------------------------------------------KOAUTOREN
    ko_titel = dflist[1].Titel.tolist()
    ko_autStatus = dflist[1].Autor_Status.tolist()
    ko_oaStatus = Listen_Ranking(dflist[1].OA_Status.tolist())
    ko_jahr = dflist[1].Jahr.tolist()
    ko_monat = dflist[1].Monat.tolist()
    ko_journal = Listen_Ranking(dflist[1].Journal.tolist())
    ko_disz = Listen_Ranking(dflist[1].Disziplin.tolist())
    ko_pub = Listen_Ranking(dflist[1].Publisher.tolist())
    ko_fa = Listen_Ranking(dflist[1].Funding_Acknowledgement.tolist())
    ko_autName = dflist[1].Name.tolist()
    # ---------------------------------------------------------------------SCHREIBEN DER ERGEBNISSE IN ANALYSE-FILE(CSV)
    erstautor = [
        getlist(oaStatus)[0],
        getlist(oaStatus)[1],
        getlist(journal)[0],
        getlist(journal)[1],
        getlist(pub)[0],
        getlist(pub)[1],
        getlist(disz)[0],
        getlist(disz)[1]]
    koautor = [
        getlist(ko_oaStatus)[0],
        getlist(ko_oaStatus)[1],
        getlist(ko_journal)[0],
        getlist(ko_journal)[1],
        getlist(ko_pub)[0],
        getlist(ko_pub)[1],
        getlist(ko_disz)[0],
        getlist(ko_disz)[1]]
    export_data = zip_longest(*erstautor, fillvalue='')
    export_data2 = zip_longest(*koautor, fillvalue='')
    with open('analysefromGUI.csv', 'w', encoding="ISO-8859-1", newline='') as out:
        wr = csv.writer(out)
        wr.writerow(['Max OA-Status'])
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
    anzEA.configure(text=' :' + str(len(titel)))
    anzKO.configure(text=' :' + str(len(ko_titel)))
    print(len(ko_titel))

#--------------------------------------------------------------------------------------------------------------PARAMETER
def regex_pattern():
    Erstautoren_regex = re.compile(r'.*%s.*' % sb()[0], re.IGNORECASE)
    Koautoren_regex = re.compile(r'.*\s\(Reprint\sAuthor\).*%s.*\.' % sb()[1], re.IGNORECASE)
    return Erstautoren_regex, Koautoren_regex
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
            if regex_pattern()[0].match(add):
                if aut not in Autoren_Collection:                                                  #Doubletten Kontrolle
                    Autoren_Collection.append(aut)
                    Autoren_Status.append('Erstautor: ' + '(' + sb()[0] + ')')
            if regex_pattern()[1].match(add2):
                Autoren_Collection.append(aut)
                Autoren_Status.append('Reprint-Autor: ' + '(' + sb()[1] + ')')
    return Autoren_Collection, Autoren_Status
#-------------------------------------------------------------------------------------
def get_max(a):
    most = max(a, key=a.get)
    all_values = a.values()
    max_value = max(all_values)
    return most, max_value

'''
Die Funktion "getlist" erzeugt zwei Listen aus dem Dict welches mit der Funktion "Listen_Ranking" erstellt wurde.
Die erste Liste beinhaltet die Keys die zweite Liste die Values. Also eine Liste mit Namen und eine Liste mit deren
Anzahl.
'''

def getlist(a):
    temp1 = []
    temp2 = []
    for key in a:
        temp1.append(key)
    for val in a.values():
        temp2.append(val)
    return temp1, temp2
#------------------------------------------------------------------------------------------------LISTEN-RANKING-FUNKTION
def Listen_Ranking(v):
    z = 0
    counter = []
    for x in v:
        x = v.count(v[z])
        z += 1
        counter.append(x)
        dictionary = dict(zip(v, counter))
    return(dictionary)
#print('Gefundene Eintraege: ' + str(Listen_Ranking(Autoren_Status)))
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
'''
#Die Funktion "MonthtoNumber" ersetzt die ausgeschrieben Monatsnamen durch die jeweilige Monatszahl
'''
def MonthtoNumber(m):
    MoNu = [(1, 'JAN'), (2, 'FEB'),
            (3, 'MÄR'), (4, 'APR'),
            (5, 'MAY'), (6, 'JUN'),
            (7, 'JUL'), (8, 'AUG'),
            (9, 'SEP'), (10, 'OKT'),
            (11, 'NOV'), (12, 'DEZ')]
    translate = []
    for l in m:
        for x in MoNu:
            if x[1] == l:
                v = l.replace(l, str(x[0]))
                translate.append(v)
    return translate
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
#pprint.pprint(Collect_FA(Autoren))
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
#----------------------------------------------------------------------------------------------------------GUI-SCHLIEßEN
def close_window():
    window.destroy()
#----------------------------------------------------GUI----------------------------------------------------------------
window = Tk()
window.geometry('1000x800')
window.title('WOS-Wandler_Alpha')


lbl = Label(window, text='', font=('Arial Bold', 10))
lbl.grid(column=0, row=0, sticky=W)
lbl2 = Label(window, text='Hier kann sowohl nach der Institution des Erst-\n als auch des Koautors gesucht werden:')
lbl2.grid(column=0, row=1, padx=0, pady=10, sticky=W)
#-------------------------------------------------------------------------------------------------------------------MENU
menu = Menu(window)

new_item = Menu(menu, tearoff=0)

new_item.add_command(label='Info')

new_item.add_separator()

new_item.add_command(label='Programm Schließen', command=close_window)

menu.add_cascade(label='Datei', menu=new_item)

window.config(menu=menu)



#Auswahl des directorys der Daten
dirlbl = Label(window, text='Bitte den Ordner Auswählen welcher die BibTex files enthält.')
dirlbl.grid(column=0, row=3, padx=0, pady=10, sticky=W)

dirbtn = Button(window, text='Verzeichnis wählen', command=selectDir)
dirbtn.grid(column=1, row=3, sticky=W)

ausbtn = Label(window, text='')
ausbtn.grid(column=3, row=3, sticky=W)

#--------------------------------------------------------------------------------------------------SUCHE-EINGABE TKINTER
#Suche nach Erstautor
lbl2 = Label(window, text='Such nach Institution Erstautor:')
lbl2.grid(column=0, row=4, padx=0, pady=10, sticky=W)

EASB = Entry(window, width=20)
EASB.grid(column=1, row=4, sticky=W)

EAanzeige = Label(window, text='__________')
EAanzeige.grid(column=3, row=4, sticky=W)


#Suche nach Koautor
lbl2 = Label(window, text='Such nach Institution Koautor:')
lbl2.grid(column=0, row=5, sticky=W)

KASB = Entry(window, width=20)
KASB.grid(column=1, row=5, sticky=W)

KAanzeige = Label(window, text='__________')
KAanzeige.grid(column=3, row=5, sticky=W)

EAbtn = Button(window, text='Suchparameter bestätigen', command=sb)
EAbtn.grid(column=1, row=6, padx=0, pady=10 ,sticky=W)

#Start BUTTON
startbtn = Button(window, text='Extraktion starten', command=start)
startbtn.grid(column=1, row=7, padx=0, pady=10, sticky=W)


#Anzeige der Daten

anzLBL = Label(window, text='Gefundene Erstautoren:')
anzLBL.grid(column=0, row=8, sticky=W)

anzEA = Label(window, text='')
anzEA.grid(column=1, row=8, padx=0, pady=10, sticky=W)

anzLBLko = Label(window, text='Gefundene Koautoren:')
anzLBLko.grid(column=0, row=9, sticky=W)

anzKO = Label(window, text='')
anzKO.grid(column=1, row=9, padx=0, pady=10, sticky=W)















window.mainloop()