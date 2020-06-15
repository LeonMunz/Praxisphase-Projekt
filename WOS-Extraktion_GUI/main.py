import bibtexparser
import glob
import os
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import csv
from itertools import zip_longest
import pandas as pd
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from collections import OrderedDict


# give value to empty vars
ea = None
ka = None
sdir = None
sdir_res = None
von = None
bis = None




def startwindow():
##### FUNKTIONEN--------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
    def close_window():
        window.destroy()
        os.remove('./Zusammengeführte_Files/collection.txt')

#-----------------------------------------------------------------------------------------------------------------------
    #Funktion zur Auswahl des Pfades in welchem die BibTex-Files liegen:
        #Sobald ein Pfad gewählt wurde, wird der "witerbtn" aktiviert.
    def selectDir():
        global sdir
        global data_clean
        sdir = filedialog.askdirectory()
        dir_lbl.configure(text=sdir, fg='green2')
        weiterbtn.configure(text='   Weiter   ', bg='white', fg='black', command=secondWindowblue)

        for filename in glob.glob(os.path.join(sdir, '*.txt')):
            print('Dateien werden zusammengeführt')
            with open(filename, 'r') as f:
                with open('./Zusammengeführte_Files/collection.txt', 'a') as outfile:
                    for line in f:
                        outfile.write(line)
        print('Collection_File_erstelllt')

        # ReGeX Pattern für das Filtern der OA-Status:
        Other_Gold_regex = re.compile(r'.*Other Gold.*', re.IGNORECASE)
        DOAJ_Gold_regex = re.compile(r'.*DOAJ Gold.*', re.IGNORECASE)
        Green_Accepted_regex = re.compile(r'.*Green Accepted.*', re.IGNORECASE)
        Green_Published_regex = re.compile(r'.*Green Published.*', re.IGNORECASE)
        Bronze_regex = re.compile(r'.*Bronze.*', re.IGNORECASE)

        data_file = './Zusammengeführte_Files/collection.txt'

        df = pd.read_csv(data_file, sep='\\t', engine='python')

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        # NaN Werte zum DataFrame hinzufügen um diese selektieren zu können:
        df_nan = df.fillna("NaN")
        # NaN Werte in der Col PY (Jahre) in 0 wandeln
        df_nan['PY'] = df_nan['PY'].replace('NaN', 0)
        # Float Werte aus der Col PY (Jahre) in Int wandeln
        df_nan['PY'] = df_nan['PY'].astype(int)

        # Alle Einträge aus DF herausnehmen die keinen OA-Status haben:
        data_only_OA = df_nan.loc[df_nan['OA'] != 'NaN']

        # DataFrame anordnen:
        data_clean = data_only_OA[['TI', 'AF', 'C1', 'RP', 'SC', 'SO', 'FU', 'PU', 'PY', 'DT', 'OA']]

        # Funktion um OA Status zu filtern und in einzelne Listen zu transferieren
        # Diese werden im Anschluss wieder in einzlene Cols in dem DF untergebracht
        def collect_oa_status(status):
            # Listen für den filter der OA-Status:
            Other_Gold = []
            DOAJ_Gold = []
            Green_Accepted = []
            Green_Published = []
            Bronze = []
            for oa_status in status:
                if Other_Gold_regex.match(oa_status):
                    Other_Gold.append('True')
                else:
                    Other_Gold.append('False')
                if DOAJ_Gold_regex.match(oa_status):
                    DOAJ_Gold.append('True')
                else:
                    DOAJ_Gold.append('False')
                if Green_Accepted_regex.match(oa_status):
                    Green_Accepted.append('True')
                else:
                    Green_Accepted.append('False')
                if Green_Published_regex.match(oa_status):
                    Green_Published.append('True')
                else:
                    Green_Published.append('False')
                if Bronze_regex.match(oa_status):
                    Bronze.append('True')
                else:
                    Bronze.append('False')
            return Other_Gold, DOAJ_Gold, Green_Published, Green_Accepted, Bronze

        # Filtern der Erstautor Institution
        # Angewendet auf die Col "C1"
        bar = data_clean['C1'].tolist()


        def institut(cone):
            institution = []
            for eai in cone:
                pattern = re.findall('\].+,\s', eai)
                for x in pattern:
                    x = x.split(',')
                    x = x[0].replace(']', '')
                    institution.append(x)
            return institution

        # Filtern der Reprintautor Institution
        # Angewendet auf die Col "RP"
        re_inst_raw = data_clean['RP'].tolist()

        def rp_inst():
            global rep_inst
            rep_inst = []
            for re_inst in re_inst_raw:
                pattern = re.findall('\),\s.+', re_inst)
                for x in pattern:
                    x = x.split(',')
                    x = x[1]
                    rep_inst.append(x)
            return rep_inst
        rp_inst()

        pattern = re.compile(r']\s([^,]+),')
        ko_aut_li = []

        for koaut in data_clean['C1']:
            ko = pattern.findall(koaut)
            ko_aut_li.append(ko)

        # Erzeugen neuer Columns im DF für Institution des Erstautors:
        data_clean['EA Institution'] = institut(bar)
        data_clean['RP Institution'] = rep_inst
        data_clean['KoAut Institution'] = ko_aut_li
        # data_clean['Koautor Institution'] = ko_aut_inst
        # Erzeugen neuer Columns im DF für OA-Status Erstautor:
        data_clean['Other Gold'] = collect_oa_status(data_clean['OA'])[0]
        data_clean['DOAJ Gold'] = collect_oa_status(data_clean['OA'])[1]
        data_clean['Green Published'] = collect_oa_status(data_clean['OA'])[2]
        data_clean['Green Accepted'] = collect_oa_status(data_clean['OA'])[3]
        data_clean['Bronze'] = collect_oa_status(data_clean['OA'])[4]

        #print(data_clean)


#-----------------------------------------------------------------------------------------------------------------------
    #Funktion zur Auswahl des Pfades für das Ergebnis-File:
    def selectDir_result():
        global sdir_res
        sdir_res = filedialog.askdirectory()
        dir_lbl_res.configure(text=sdir_res, fg='green2')
        return sdir_res
#-----------------------------------------------------------------------------------------------------------------------
    #Funktion für die Fehlermeldung, dass nooch kein Pfad für die BibTex-Files angegeben wurde:
    def kontrol_dir():
        dir_lbl.configure(text='Bitte wählen Sie zu erst ein Verzeichnis.', fg='red')


#-----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------EINGABE-DER-SUCHPARAMETER-IN-GUI
    '''
    Die Funktion "sb" (search bar) ermöglicht die eingabe der Suchparameter via grafischer Oberfläche
    '''
    def sb():
        global ea
        global ka

        if entry_ea.get():
            ea = entry_ea.get()
            entry_ea_choice_lbl.configure(text=ea, fg='green')
        else:
            entry_ea_choice_lbl.configure(text='Eine Eingabe beider Felder wird benötigt', anchor='e', fg='red')
        if entry_ko.get():
            ka = entry_ko.get()
            entry_ko_choice_lbl.configure(text=ka, fg='green')
        else:
            entry_ko_choice_lbl.configure(text='Eine Eingabe beider Felder wird benötigt', anchor='e', fg='red')

        return ea, ka
#-----------------------------------------------Extraction Functions----------------------------------------------------

    #Variablen:

    MoNu = [(1, 'JAN'), (2, 'FEB'),
            (3, 'MAR'), (4, 'APR'),
            (5, 'MAY'), (6, 'JUN'),
            (7, 'JUL'), (8, 'AUG'),
            (9, 'SEP'), (10, 'OKT'),
            (11, 'NOV'), (12, 'DEZ')]


    # Nur für den print Befehl, kann später rausgenommen werden
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    def extended_sear():
        global von
        global bis

        if date_search_from.get():
            von = int(date_search_from.get())
            resul_date_von.configure(bg='grey19', fg='green2', text=von)
        if date_search_to.get():
            bis = int(date_search_to.get())
            resul_date_bis.configure(bg='grey19', fg='green2', text=bis)
        print(von + bis)


    def main_extraction():
        global Titel
        global Titel_ka
        global dopplung
        global mix_li
        global ea_li
        global ka_li


        global ea_oa_status_collect
        global rp_oa_status_collect

        global data_select_inst_ea
        global data_select_inst_rp

        global gesamte_ea_rows
        global gesamte_rp_rows
        #Variablen für Kooperationen:
        global li_ordered_koop
        global count_gem_koom_mit_ea



        # Regex Pattern für die Suche nach der Erstautor Institution:
        Erstautoren_regex = re.compile(r'.*%s.*' % ea, re.IGNORECASE)
        Koautoren_regex = re.compile(r'.*%s.*' % ka, re.IGNORECASE)


        if von is None:
            # Abfrage nach Erstautoren Regex:
            # Dataframe für die Analyse über Erstautoren:
            data_select_inst_ea = data_clean.loc[data_clean['EA Institution'].str.match(Erstautoren_regex) == True]
            data_select_inst_ea['Aut-Status'] = 'Erstautor'

            # Abfrage nach Reprint-Autoren Regex:
            # Datafram für die Analyse über Reprintautoren:
            data_select_inst_rp = data_clean.loc[data_clean['RP Institution'].str.match(Koautoren_regex) == True]
            data_select_inst_rp['Aut-Status'] = 'Reprint-Autor'

            print('Outfile erstellt ohne erweiterte Such-Parameter erstellt')
        else:
            gather_Date = (data_clean.loc[(data_clean['PY'] >= von) & (data_clean['PY'] <= bis)])

            data_select_inst_ea = gather_Date[data_clean['EA Institution'].str.match(Erstautoren_regex) == True]
            data_select_inst_ea['Aut-Status'] = 'Erstautor'

            data_select_inst_rp = gather_Date[data_clean['EA Institution'].str.match(Koautoren_regex) == True]
            data_select_inst_rp['Aut-Status'] = 'Reprint-Autor'






        complete_set = pd.concat([data_select_inst_ea, data_select_inst_rp])
        complete_set.to_csv('main_ausgabe_file.csv')

        print(complete_set)
        # OUTFILE ERSTELLEN

        # Die Funktion "count_oa_status" zählt die mit True angegebenen Einträge im DF
        def count_oa_status(anz):
            anzahl = 0
            anzwrong = 0
            for x in anz:
                if x == 'True':
                    anzahl += 1
                else:
                    anzwrong = +1

            return anzahl




        ea_other_gold = count_oa_status(data_select_inst_ea['Other Gold'])
        ea_doaj_gold = count_oa_status(data_select_inst_ea['DOAJ Gold'])
        ea_green_published = count_oa_status(data_select_inst_ea['Green Published'])
        ea_green_accepted = count_oa_status(data_select_inst_ea['Green Accepted'])
        ea_bronze = count_oa_status(data_select_inst_ea['Bronze'])

        rp_other_gold = count_oa_status(data_select_inst_rp['Other Gold'])
        rp_doaj_gold = count_oa_status(data_select_inst_rp['DOAJ Gold'])
        rp_green_published = count_oa_status(data_select_inst_rp['Green Published'])
        rp_green_accepted = count_oa_status(data_select_inst_rp['Green Accepted'])
        rp_bronze = count_oa_status(data_select_inst_rp['Bronze'])



        ea_oa_status_collect = [ea_other_gold, ea_doaj_gold, ea_green_published, ea_green_accepted, ea_bronze]
        rp_oa_status_collect = [rp_other_gold, rp_doaj_gold, rp_green_published, rp_green_accepted, rp_bronze]

        # Variablen um Anzahl im "Result-Window" anzuzeigen:
        gesamte_ea_rows = len(data_select_inst_ea['TI'])
        gesamte_rp_rows = len(data_select_inst_rp['TI'])

        mix_rows = gesamte_ea_rows + gesamte_rp_rows


        # Filtern der in beiden Kategorien (Erst- Redprint-Autor) vorkommenden Einträge:
        dopplung = 0
        for x in data_select_inst_ea['TI']:
            for y in data_select_inst_rp['TI']:
                if x == y:
                    dopplung += 1

        print(data_select_inst_ea)

        # Auswertung der Kooperationen zwischen den Instituten (Erst- Koautor)

        def Listen_Ranking(v):
            z = 0
            counter = []
            for x in v:
                x = v.count(v[z])
                z += 1
                counter.append(x)
                out = dict(zip(v, counter))
            return (out)

        #hier muss die liste aus dem df rein das schon gefiltert wurde!!!!!!!!!!!!!!!!
        collect_koautli = []
        for x in data_select_inst_ea['KoAut Institution'].tolist():
            for y in x:
                collect_koautli.append(y)

        sortierte_koop = OrderedDict(sorted(Listen_Ranking(collect_koautli).items(), key=lambda x: x[1], reverse=True))

        #Liste zur Ausgabe der nach häufigkeit sortierten meisten Kooperationen
        li_ordered_koop = []
        count_gem_koom_mit_ea = 0
        for b in sortierte_koop:
            li_ordered_koop.append(b)
            if Erstautoren_regex.match(b):
                count_gem_koom_mit_ea += 1

        print(count_gem_koom_mit_ea)













        os.remove('./Zusammengeführte_Files/collection.txt')
        print('Collection-File gelöscht')
        result_window()

#-----------------------------------------------------------------------------------------------------------------------
#Fenster:
    def mainWindowGrey():

        #globale Variablen deklarieren
        global sdir
        global dir_lbl
        global weiterbtn
        global dir_lbl_res

#---------------------------------------------------FRAMES--------------------------------------------------------------
        #Display Frames (Main size 900, 550))):
            #Base Frame:
        base_Frame = Frame(window, width=900, height=550, bg='grey19')

            #Center Frames:
        base_Frame_left = Frame(base_Frame, width=100, height=380, bg='grey16')
        base_Frame_rigth = Frame(base_Frame, width=100, height=380, bg='grey16')
        base_Frame_center = Frame(base_Frame, width=600, height=380, bg='grey16')

            #Top Frames:
        top_Frame = Frame(window, width=900, height=80, highlightbackground="grey19",
                          highlightthickness=1, bg='grey16')
        top_Frame_center = Frame(top_Frame, width=640, height=80, bg='grey16')
        top_Frame_left = Frame(top_Frame, width=100, height=80, bg='blue')
        top_Frame_right = Frame(top_Frame, width=100, height=80, bg='green')

            #Bottom Frames:
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20",
                             highlightthickness=1, bg='grey16')

        bottom_space_Frame_left = Frame(bottom_Frame, width=532, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=80, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        #Positioning Frames:
            #Base Frames:
        base_Frame.grid_rowconfigure(0, weight=1)
        base_Frame.grid_columnconfigure(1, weight=1)

        base_Frame.grid(row=1, column=0, sticky='nsew')

            #Top Frame:
        top_Frame.grid(row=0, column=0, sticky='ew')
        top_Frame_center.grid(row=0, column=0, sticky='ew')
        top_Frame_left.grid(row=0, column=1, sticky='w')
        top_Frame_right.grid(row=0, column=2, padx=15, sticky='e')

            #Side Frames:
        base_Frame_left.grid(row=0, column=0, sticky='ns')
        base_Frame_rigth.grid(row=0, column=2, sticky='ns')

            #Center Frame:
        base_Frame_center.grid(row=0, column=1, sticky='nsew')

            #Bottom Frames:
        bottom_Frame.grid(column=0, row=2, sticky='esw')
        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')

#-------------------------------------------------CONTENT---------------------------------------------------------------
        #BTNS Display:
            #BTNs in Center:
        dir_btn = Button(base_Frame_center, text='Verzeichnis wählen', command=selectDir)
        dir_btn_result = Button(base_Frame_center, text='Verzeichnis wählen', command=selectDir_result)

            #BTNs in Bottom Frame
        if sdir is not None:
            weiterbtn = Button(bottom_button_Frame_forw, bg='white', fg='black', text='   Weiter   ',
                               command=secondWindowblue)
        else:
            weiterbtn = Button(bottom_button_Frame_forw, bg='grey17', fg='gray33', text='   Weiter   ', command=kontrol_dir)

        #BTNS Position
            #BTNS in Center:
        dir_btn.grid(row=2, column=0, sticky='w')
        dir_btn_result.grid(row=4, column=0, sticky='w')

            #BTNs in Bottom Frame:
        weiterbtn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')
        bottom_button_Frame_forw.grid_propagate(0)

        #Display Labels:
        wel_lbl = Label(base_Frame_center, fg='white smoke', bg='grey16', justify=LEFT, text=
        'Willkommen bei WOSAT (Web of Science analyse tool).                                 \n'
        'Um eine Analyse zu ermöglichen, müssen die von ihnen heruntergeladenen Files im BibTex-\n'
        'Format vorliegen. Die einzelnen Files können Sie in Sets von jeweils 500 Einträgen bei WOS herunterladen.\n'
        'www.webofknowledge.com\n'
                        )

        instruction_lbl = Label(base_Frame_center, fg='white smoke', bg='grey16', justify=LEFT, text=
        ' \n'
        'Bitte wählen Sie das Verzeichnis in dem sich die einzelnen BibTex-Files befinden: \n'
        ' '
                                )

        result_dir_lbl = Label(base_Frame_center, fg='white smoke', bg='grey16', justify=LEFT, text=
        '\n'
        '\n'
        'Bitte wählen Sie das Verzeichnis in dem die Ergebnisfiles abgelegt werden sollen:'
        '\n'
        '*Falls keine Auswahl getroffen wird, werden die Files im Programmordner abgelegt'
        '\n'
                               )

        #Labels Position
            #Label in Center
        if sdir is not None:
            dir_lbl = Label(base_Frame_center, text=sdir, fg='green2', bg='grey19')
        else:
            dir_lbl = Label(base_Frame_center, text='                      ', fg='green2', bg='grey19')
        if sdir_res is not None:
            dir_lbl_res = Label(base_Frame_center, text=sdir_res, fg='green2', bg='grey19')
        else:
            dir_lbl_res = Label(base_Frame_center, text='                       ', fg='green2', bg='grey19')

        # Positioning Content
            #Center
        wel_lbl.grid(row=0, columnspan=2, sticky='wn')
        instruction_lbl.grid(row=1, columnspan=2, sticky='w')
        result_dir_lbl.grid(row=3, columnspan=2, sticky='w')

        dir_lbl.grid(row=2, column=1, sticky='w')
        dir_lbl_res.grid(row=4, column=1, sticky='w')
            #IMG:
        img = ImageTk.PhotoImage(Image.open("./img/Logo_ULB.png"))
        panel = Label(top_Frame_left, image=img)
        panel.photo = img
        panel.grid(row=0, column=0)

        img = ImageTk.PhotoImage(Image.open("TH_Koeln_Logo.png"))
        panel = Label(top_Frame_right, image=img)
        panel.photo = img
        panel.grid(row=0, column=0)


#-----------------------------------------------------------------------------------------------------------------------
    def secondWindowblue():
        # Globale Variablen deklarieren
        global entry_ea
        global entry_ea_choice_lbl
        global entry_ko
        global entry_ko_choice_lbl
        global ea
        global ka
#---------------------------------------------------FRAMES--------------------------------------------------------------
        # Display Frames (Main size 900, 550))):
        # Base Frame:
        base_Frame = Frame(window, width=900, height=550, bg='grey19')

        # Center Frames:
        base_Frame_left = Frame(base_Frame, width=100, height=380, bg='grey16')
        base_Frame_rigth = Frame(base_Frame, width=100, height=380, bg='grey16')
        base_Frame_center = Frame(base_Frame, width=600, height=380, bg='grey16')

        center_Frame_top = Frame(base_Frame_center, width=700, height=90, bg='grey16')
        center_Frame_left = Frame(base_Frame_center, width=280, height=300, bg='grey16')
        center_Frame_right = Frame(base_Frame_center, width=210, height=300, bg='grey16')
        center_Frame_com = Frame(base_Frame_center, width=210, height=300, bg='grey16')

        # Top Frames:
        top_Frame = Frame(window, width=900, height=80, highlightbackground="grey19",
                          highlightthickness=1, bg='grey16')
        top_Frame_center = Frame(top_Frame, width=540, height=80, bg='grey16')
        top_Frame_left = Frame(top_Frame, width=100, height=80, bg='grey16')
        top_Frame_left_logo = Frame(top_Frame, width=100, height=80, bg='grey16')
        top_Frame_right_logo = Frame(top_Frame, width=100, height=80, bg='grey16')

        # Bottom Frames:
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20",
                             highlightthickness=1, bg='grey16')

        bottom_space_Frame_left = Frame(bottom_Frame, width=532, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=80, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')
        bottom_button_Frame_back.grid_propagate(0)
        bottom_button_Frame_forw.grid_propagate(0)

        # Positioning Frames:
        # Base Frames:
        base_Frame.grid_rowconfigure(0, weight=1)
        base_Frame.grid_columnconfigure(1, weight=1)

        base_Frame.grid(row=1, column=0, sticky='nsew')

        # Top Frame:
        top_Frame.grid(row=0, column=0, sticky='ew')
        top_Frame_center.grid(row=0, column=1, sticky='ew')
        top_Frame_center.grid_propagate(0)
        top_Frame_left.grid(row=0, column=0)
        top_Frame_left_logo.grid(row=0, column=2, sticky='w')
        top_Frame_right_logo.grid(row=0, column=3, padx=15, sticky='e')

        # Side Frames:
        base_Frame_left.grid(row=0, column=0, sticky='ns')
        base_Frame_rigth.grid(row=0, column=2, sticky='ns')

        # Center Frame:
        base_Frame_center.grid(row=0, column=1, sticky='nsew')

        center_Frame_top.grid(row=0, columnspan=3, sticky='n')
        center_Frame_left.grid(row=1, column=0, sticky='w')
        center_Frame_right.grid(row=1, column=1, sticky='w')
        center_Frame_com.grid(row=1, column=2, sticky='w')
        center_Frame_top.grid_propagate(0)
        center_Frame_left.grid_propagate(0)
        center_Frame_right.grid_propagate(0)
        center_Frame_com.grid_propagate(0)

        # Bottom Frames:
        bottom_Frame.grid(column=0, row=2, sticky='esw')
        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')
# ------------------------------------------------CONTENT---------------------------------------------------------------
        #Entry fields display:
        entry_ea = Entry(center_Frame_left, width=20)
        entry_ko = Entry(center_Frame_left, width=20)

        # BTNS Display:
            # BTNs in Center:
        choose_btn = Button(center_Frame_left, text='  Eingabe Bestätigen  ', command=sb)
        extendet_search_btn = Button(center_Frame_left, text='    Erweiterte Suche    ', command= extendet_search)


            # BTNs in Bottom Frame
        weiterbtn = Button(bottom_button_Frame_forw, text='Starten', command=main_extraction)
        back_btn = Button(bottom_button_Frame_back, text='   Zurück   ', command=mainWindowGrey)

        # BTNS Position
            # BTNS in Center:
        choose_btn.grid(row=4, column=1, pady=10, sticky='w')
        extendet_search_btn.grid(row=5, column=1, pady=50, sticky='w')


            # BTNs in Bottom Frame:
        weiterbtn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')
        back_btn.grid(column=0, row=0, padx=0, pady=5, sticky='nwse')

        # Display Labels:
            #Top
        head_lbl = Label(top_Frame_center, fg='white smoke', bg='grey16', text= '\n\nAuswahl der institution und Erweiterte Suche:')
            #Center
        wel_lbl = Label(center_Frame_top, fg='white smoke', bg='grey16', justify=LEFT, text=
        '\nHier kommt ein angenehm inhaltsschwangerer, informativer Text zum Einsatz\n'
        'Dieser muss nur noch von der entsprechenden Person verfasst werden.\n'
                        )

        nfo_lbl = Label(center_Frame_top, bg='grey16', fg='white smoke', text=
        'Eingabe der zu suchenden Institutionen:\n')

        entry_ea_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', justify=LEFT, text=
        'Institution Erstautor: ')
        entry_ko_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', justify=LEFT, text=
        'Institution Koautor: ')

        if ea is not None:
            entry_ea_choice_lbl = Label(center_Frame_right, bg='grey19', fg='green', justify=LEFT,
                                        text=ea, textvariable=ea)
        else:
            entry_ea_choice_lbl = Label(center_Frame_right, bg='grey19', fg='white smoke', justify=LEFT,
                                        text='     TEST     ')
        if ka is not None:
            entry_ko_choice_lbl = Label(center_Frame_right, bg='grey19', fg='green', justify=LEFT,
                                        text=ka)
        else:
            entry_ko_choice_lbl = Label(center_Frame_right, bg='grey19', fg='white smoke', justify=LEFT,
                                        text='     TEST     ')

        sear_vorschläge = Label(center_Frame_com, bg='grey19', fg='white smoke', justify=LEFT,
                                        text='Vorschlag:')
        # Labels Position
            #Labels in Top:
        head_lbl.grid(row=0, column=0, sticky='s')
            # Label in Center
        wel_lbl.grid(row=0, columnspan=3, sticky='wn')

        entry_ea_lbl.grid(row=1, column=0, sticky='w')
        entry_ko_lbl.grid(row=2, column=0, sticky='w')

        nfo_lbl.grid(row=1, column=0, sticky='w')

        entry_ea_choice_lbl.grid(row=0, column=0, pady=20, sticky='w')
        entry_ko_choice_lbl.grid(row=1, column=0, padx=0, sticky='w')

        sear_vorschläge.grid(row=0, column=0)

        # Positioning Content
        # Center
        entry_ea.grid(row=1, column=1, pady=20, sticky='news')
        entry_ko.grid(row=2, column=1, sticky='news')

        # IMG:
        img = ImageTk.PhotoImage(Image.open("./img/Logo_ULB.png"))
        panel = Label(top_Frame_left_logo, image=img)
        panel.photo = img
        panel.grid(row=0, column=0)

        img = ImageTk.PhotoImage(Image.open("TH_Koeln_Logo.png"))
        panel = Label(top_Frame_right_logo, image=img)
        panel.photo = img
        panel.grid(row=0, column=0)

# ----------------------------------------------------------------------------------------------------------------------
    def extendet_search():
        global date_search_from
        global date_search_to
        global resul_date_von
        global resul_date_bis
        #Funktionen:

# ---------------------------------------------------FRAMES-------------------------------------------------------------
        center_Frame0 = Frame(window, width=800, height=550, bg='grey19')


        center_space_Frame_top = Frame(window, width=900, height=80, highlightbackground="grey20", highlightthickness=1,
                                       bg='grey16')
        center_space_Frame_left = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_rigth = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_center = Frame(center_Frame0, width=700, height=380, bg='grey16')
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20", highlightthickness=1,
                             bg='grey16')

        center_content_Frame_top = Frame(center_space_Frame_center, width=700, height=190, bg='grey16')
        center_content_Frame_bottom = Frame(center_space_Frame_center, width=700, height=190, bg='grey16')

        bottom_space_Frame_left = Frame(bottom_Frame, width=562, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=100, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        # Positioning_Frames
        center_Frame0.grid_rowconfigure(0, weight=1)
        center_Frame0.grid_columnconfigure(1, weight=1)

        center_Frame0.grid(row=1, column=0, sticky='nsew')

        center_space_Frame_left.grid(row=0, column=0, sticky='ns')
        center_space_Frame_top.grid(row=0, column=0, sticky='ew')
        center_space_Frame_rigth.grid(row=0, column=2, sticky='ns')
        center_space_Frame_center.grid(row=0, column=1, sticky='nsew')

        bottom_Frame.grid(column=0, row=2, sticky='esw')

        #content Frames


        center_content_Frame_top.grid(row=0, column=0, sticky='wn')
        center_content_Frame_bottom.grid(row=1, column=0, sticky='wn')

        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')


        #Label MAIN

        ext_search_wel_lbl = Label(center_content_Frame_top, pady=20, bg='grey16', fg='white smoke', justify=LEFT,
                                   text='Die erweiterte Suche bietet die Möglichkeit nach nach bestimmten Kriterien zu Filtern.')
        search_date_lbl = Label(center_content_Frame_top, bg='grey16', fg='white smoke', justify=LEFT,
                                text='Ergebnisse filtern nach Zeitraum der Veröffentlichung (Jahr):  ' + '\n')
        von_lbl = Label(center_content_Frame_top
                        , bg='grey16', fg='white smoke', justify=LEFT, text='Von:  ')
        bis_lbl = Label(center_content_Frame_top
                        , bg='grey16', fg='white smoke', justify=LEFT, text='Bis:  ')

        desc_oa_auswahl_lbl = Label(center_content_Frame_bottom, bg='grey16', fg='white smoke', justify=LEFT,
                                    text= '___________________________________________________________________' + '\n' +
                                    '\n' + 'Ergebnisse Filtern nach Open Access Status: ' + '\n')

        #Ergebnis Label der Datumwerte
        if von is not None:
            resul_date_von = Label(center_content_Frame_top, bg='grey19', fg='green2', text=von)
        else:
            resul_date_von = Label(center_content_Frame_top, bg='grey19', fg='green', text='Test 1')
        if bis is not None:
            resul_date_bis = Label(center_content_Frame_top, bg='grey19', fg='green2', text=bis)
            print('is da')
        else:
            resul_date_bis = Label(center_content_Frame_top, bg='grey19', fg='green', text='Test 2')
            print('is nich da')


        #Date search
        date_search_from = Entry(center_content_Frame_top)
        date_search_to = Entry(center_content_Frame_top)

        #Auswahl BTNs OA-Status
        check_btn_Other_Gold = Checkbutton(center_content_Frame_bottom, text='Other Gold')
        check_btn_DOAJ_Gold = Checkbutton(center_content_Frame_bottom, text='DOAJ Gold')
        check_btn_Green_Accepted = Checkbutton(center_content_Frame_bottom, text='Green Accepted')
        check_btn_Green_Published = Checkbutton(center_content_Frame_bottom, text='Green Published')
        check_btn_Bronze = Checkbutton(center_content_Frame_bottom, text='Bronze')

        #BTNs
        date_search_btn = Button(center_content_Frame_top, text='Auswahl bestätigen', command=extended_sear)
        oa_search_btn = Button(center_content_Frame_bottom, text='Auswahl bestätigen')
            #Bottom BTNs:
        back_btn = Button(bottom_button_Frame_back, text='   Zurück   ', command=secondWindowblue)

        #BTNs Positioning
        date_search_btn.grid(row=4, column=1, pady=3, sticky='w')
        oa_search_btn.grid(row=4, columnspan=5, pady=5, sticky='w')
            #Bottom BTNs:
        back_btn.grid(column=0, row=0, padx=0, pady=5, sticky='nwse')

        #Check BTNs
        check_btn_Other_Gold.grid(row=2, column=0, padx=0, sticky='w')
        check_btn_DOAJ_Gold.grid(row=2, column=1, padx=0, sticky='w')
        check_btn_Green_Accepted.grid(row=2, column=2, padx=0, sticky='w')
        check_btn_Green_Published.grid(row=2, column=3, padx=0, sticky='w')
        check_btn_Bronze.grid(row=2, column=4, sticky='w')

        #Label Positioning
        ext_search_wel_lbl.grid(row=0, columnspan=5, sticky='nw')
        search_date_lbl.grid(row=1, columnspan=5, sticky='w')

        von_lbl.grid(row=2, column=0, pady=3, sticky='w')
        bis_lbl.grid(row=3, column=0, sticky='w')

        resul_date_von.grid(row=2, column=2, pady=3, sticky='w')
        resul_date_bis.grid(row=3, column=2, pady=3, sticky='w')

        desc_oa_auswahl_lbl.grid(row=0, columnspan=5, sticky='w')

        #Choose Positioning
        #Date search
        date_search_from.grid(row=2, column=1, sticky='w')
        date_search_to.grid(row=3, column=1, sticky='w')

    def result_window():
        #Chart Funktions:
            #PieCharts:
        def mix_val_pie():
        # Values for PieChart
            labels = ['Other Gold', 'DOAJ Gold', 'Green Published', 'Green Accepted', 'Bronze']
            sizes = ea_oa_status_collect[0], \
                    ea_oa_status_collect[1], \
                    ea_oa_status_collect[2], \
                    ea_oa_status_collect[3], \
                    ea_oa_status_collect[4]

            colors = ['#f5ff21', '#fffb87', '#4dde93', '#67de4d', '#dea94d']
            plt.rcParams['font.size'] = 6.0
            fig1, ax1 = plt.subplots()

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%d', startangle=90)

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='darkslategrey')
            fig = plt.gcf()

            plt.title('Erstautor OA-Status Verteilung', color='white')

            fig.gca().add_artist(centre_circle)
            fig.patch.set_facecolor('darkslategrey')
            fig.set_size_inches(4, 3)
            ax1.axis('equal')

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, center_Frame_right)
            canvas.get_tk_widget().grid(row=0, column=0)
        def ea_pie():
            # Values for PieChart
            labels = ['Other Gold', 'DOAJ Gold', 'Green Published', 'Green Accepted', 'Bronze']
            sizes = rp_oa_status_collect[0], \
                    rp_oa_status_collect[1], \
                    rp_oa_status_collect[2], \
                    rp_oa_status_collect[3], \
                    rp_oa_status_collect[4]

            colors = ['#f5ff21', '#fffb87', '#4dde93', '#67de4d', '#dea94d']
            plt.rcParams['font.size'] = 6.0
            fig1, ax1 = plt.subplots()

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%d', startangle=90)

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='darkslategrey')
            fig = plt.gcf()

            plt.title('Reprint-Autor OA-Status Verteilung', color='white')

            fig.gca().add_artist(centre_circle)
            fig.patch.set_facecolor('darkslategrey')
            fig.set_size_inches(4, 3)
            ax1.axis('equal')

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, center_Frame_right)
            canvas.get_tk_widget().grid(row=0, column=0)
        def ka_pie():
            # Values for PieChart
            labels = ['Other Gold', 'DOAJ Gold', 'Green Published', 'Green Accepted', 'Bronze']
            sizes = rp_oa_status_collect[0], \
                    rp_oa_status_collect[1], \
                    rp_oa_status_collect[2], \
                    rp_oa_status_collect[3], \
                    rp_oa_status_collect[4]

            colors = ['#f5ff21', '#fffb87', '#4dde93', '#67de4d', '#dea94d']
            plt.rcParams['font.size'] = 6.0
            fig1, ax1 = plt.subplots()

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='darkslategrey')
            fig = plt.gcf()

            plt.title('Das hier nnmuss weg', color='white')

            fig.gca().add_artist(centre_circle)
            fig.patch.set_facecolor('darkslategrey')
            fig.set_size_inches(4, 3)
            ax1.axis('equal')

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, center_Frame_right)
            canvas.get_tk_widget().grid(row=0, column=0)



        # Display Frames (Main size 900, 550))):
        # Base Frame:
        base_Frame = Frame(window, width=900, height=550, bg='grey19')

        # Center Frames:
        base_Frame_left = Frame(base_Frame, width=100, height=380, bg='grey16')
        base_Frame_rigth = Frame(base_Frame, width=100, height=380, bg='grey16')
        base_Frame_center = Frame(base_Frame, width=600, height=380, bg='grey16')

        center_Frame_top = Frame(base_Frame_center, width=700, height=90, bg='grey16')
        center_Frame_left = Frame(base_Frame_center, width=270, height=150, bg='grey16')
        center_Frame_left_bottom = Frame(base_Frame_center, width=270, height=200, bg='grey16')
        center_Frame_left_bottom_one = Frame(center_Frame_left_bottom, width=135, height=200, bg='grey16')
        center_Frame_mid = Frame(base_Frame_center, width=30, height=300, bg='grey16')
        center_Frame_right = Frame(base_Frame_center, width=400, height=300, bg='grey16')

        # Top Frames:
        top_Frame = Frame(window, width=900, height=80, highlightbackground="grey19",
                          highlightthickness=1, bg='grey16')
        top_Frame_center = Frame(top_Frame, width=540, height=80, bg='grey16')
        top_Frame_left = Frame(top_Frame, width=100, height=80, bg='grey16')
        top_Frame_left_logo = Frame(top_Frame, width=100, height=80, bg='grey16')
        top_Frame_right_logo = Frame(top_Frame, width=100, height=80, bg='grey16')

        # Bottom Frames:
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20",
                             highlightthickness=1, bg='grey16')

        bottom_space_Frame_left = Frame(bottom_Frame, width=532, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=80, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')
        bottom_button_Frame_back.grid_propagate(0)
        bottom_button_Frame_forw.grid_propagate(0)

        # Positioning Frames:
        # Base Frames:
        base_Frame.grid_rowconfigure(0, weight=1)
        base_Frame.grid_columnconfigure(1, weight=1)

        base_Frame.grid(row=1, column=0, sticky='nsew')

        # Top Frame:
        top_Frame.grid(row=0, columnspan=3, sticky='ew')
        top_Frame_center.grid(row=0, column=1, sticky='ew')
        top_Frame_center.grid_propagate(0)
        top_Frame_left.grid(row=0, column=0)
        top_Frame_left_logo.grid(row=0, column=2, sticky='w')
        top_Frame_right_logo.grid(row=0, column=3, padx=15, sticky='e')

        # Side Frames:
        base_Frame_left.grid(row=0, column=0, sticky='ns')
        base_Frame_rigth.grid(row=0, column=2, sticky='ns')

        # Center Frame:
        base_Frame_center.grid(row=0, column=1, sticky='nsew')

        center_Frame_top.grid(row=0, columnspan=4, sticky='n')
        center_Frame_left.grid(row=1, column=0, sticky='nw')
        center_Frame_left_bottom.grid(row=1, column=0, sticky='sw')
        center_Frame_left_bottom_one.grid(row=0, column=0, sticky='w')
        center_Frame_mid.grid(row=1, column=1, sticky='w')
        center_Frame_right.grid(row=1, column=2, sticky='e')

        center_Frame_top.grid_propagate(0)
        center_Frame_left_bottom.grid_propagate(0)
        center_Frame_left_bottom_one.grid_propagate(0)
        center_Frame_left.grid_propagate(0)
        center_Frame_mid.grid_propagate(0)
        center_Frame_right.grid_propagate(0)

        # Bottom Frames:
        bottom_Frame.grid(column=0, row=2, sticky='esw')
        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')
    # CONtent
        wel_lbl = Label(top_Frame_center, bg='grey16', fg='white smoke', text='\n\nErgebnis Fenster: ')

    # BTNs in Bottom Frame
        weiterbtn = Button(bottom_button_Frame_forw, text='Schließen', command=close_window)
        back_btn = Button(bottom_button_Frame_back, text='   Zurück   ', command=secondWindowblue)
        weiterbtn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')
        back_btn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')

    # Content Position:
        # Top Frame:
        wel_lbl.grid(row=0, column=0)

        # IMG:
        img = ImageTk.PhotoImage(Image.open("./img/Logo_ULB.png"))
        panel = Label(top_Frame_left_logo, image=img)
        panel.photo = img
        panel.grid(row=0, column=0)

        img = ImageTk.PhotoImage(Image.open("TH_Koeln_Logo.png"))
        panel = Label(top_Frame_right_logo, image=img)
        panel.photo = img
        panel.grid(row=0, column=0)
    # Results LBL:
        ea_sum_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', text='Erstautoren der Institution:  ' + str(ea))
        ka_sum_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', text='Koautoren der Institution:  ' + str(ka))
        dopp_sum_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', text='Dopplungen:')
        koop_anz_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', text='Kooperation mit: ' + str(ea))


        #Result Position LBL:
        ea_sum_lbl.grid(row=0, column=0, sticky='w')
        ka_sum_lbl.grid(row=1, column=0, sticky='w')
        dopp_sum_lbl.grid(row=2, column=0, sticky='w')
        koop_anz_lbl.grid(row=3, column=0, sticky='w')
    #Chart BTNs:
        pie_chart_mix_btn = Button(center_Frame_left_bottom_one, text=' Erstautor ', command=mix_val_pie)
        pie_chart_ea_btn = Button(center_Frame_left_bottom_one, text=' Reprint-Autor ', command=ea_pie)

        koop_li_btn = Button(center_Frame_left_bottom_one, text=' Kooperationen ', command=mix_val_pie)


    # Chart BTNs Position:
        pie_chart_mix_btn.grid(row=1, column=0, pady=2, sticky='w')
        pie_chart_ea_btn.grid(row=2, column=0, sticky='w')
        koop_li_btn.grid(row=3, column=0, sticky='w')


    # Results VALUEs

        ea_sum_val = Label(center_Frame_mid, bg='white smoke', fg='black', text=str(gesamte_ea_rows))
        ka_sum_val = Label(center_Frame_mid, bg='white smoke', fg='black', text=str(gesamte_rp_rows))
        dopp_sum_val = Label(center_Frame_mid, bg='white smoke', fg='black', text=str(dopplung))
        anz_koop_val = Label(center_Frame_mid, bg='white smoke', fg='black', text=str(count_gem_koom_mit_ea))

        pie_desc_lbl = Label(center_Frame_left_bottom_one, bg='grey16', fg='white smoke', text='OA-Status PieCharts:')

        pie_desc_lbl.grid(row=0, column=0, sticky='w')
    # Results VALUEs Position:
        ea_sum_val.grid(row=0, column=0, sticky='w')
        ka_sum_val.grid(row=1, column=0, sticky='w')
        dopp_sum_val.grid(row=2, column=0, sticky='w')
        anz_koop_val.grid(row=3, column=0, sticky='w')

    # Setup for Piechart:
    # PieChart Built in
        def pie_present(pie_oa):
            pie_oa_stat = []
            for status in pie_oa:
                if status == 'True':
                    pie_oa_stat.append('True')
            return pie_oa_stat

        def mix_val_pie():
        # Values for PieChart
            labels = ['Other Gold', 'DOAJ Gold', 'Green Published', 'Green Accepted', 'Bronze']
            sizes = ea_oa_status_collect[0], \
                    ea_oa_status_collect[1], \
                    ea_oa_status_collect[2], \
                    ea_oa_status_collect[3], \
                    ea_oa_status_collect[4]


            colors = ['#f5ff21', '#fffb87', '#4dde93', '#67de4d', '#dea94d']
            plt.rcParams['font.size'] = 6.0
            fig1, ax1 = plt.subplots()

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%d', startangle=90)

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='darkslategrey')
            fig = plt.gcf()

            plt.title('Erstautor OA-Status Verteilung', color='white')

            fig.gca().add_artist(centre_circle)
            fig.patch.set_facecolor('darkslategrey')
            fig.set_size_inches(4, 3)
            ax1.axis('equal')

            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, center_Frame_right)
            canvas.get_tk_widget().grid(row=0, column=0)
        mix_val_pie()

    window = Tk()
    window.geometry('{}x{}'.format(900, 550))
    #window.resizable(0, 0)
    window.title('WOSAT_Alpha')

    # Menu
    menu = Menu(window)
    new_item = Menu(menu, tearoff=0)
    new_item.add_command(label='Info')

    new_item.add_separator()

    new_item.add_command(label='Programm Schließen', command=close_window)
    menu.add_cascade(label='Datei', menu=new_item)
    window.config(menu=menu)

    #secondWindowblue()
    mainWindowGrey()
    #result_window()
    #thirdwindow()


    window.mainloop()

startwindow()