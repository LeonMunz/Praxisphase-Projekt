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
        #Regex-Pattern:
        Erstautoren_regex = re.compile(r'.*%s.*' % ea, re.IGNORECASE)
        Koautoren_regex = re.compile(r'.*\s\(Reprint\sAuthor\).*%s.*\.' % ka, re.IGNORECASE)

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

        # Alle Einträge aus DF herausnehmen die keinen OA-Status haben:
        data_only_OA = df_nan.loc[df_nan['OA'] != 'NaN']

        # Abfrage nach Koautoren Regex:
        data_select_inst_ka = data_only_OA.loc[data_only_OA['RP'].str.match(Koautoren_regex) == True]

        # Abfrage nach Erstautoren Regex:
        data_select_inst_ea = data_only_OA.loc[data_only_OA['C1'].str.match(Erstautoren_regex) == True]

        # Erstautoren Listen:
        Titel = data_select_inst_ea['TI'].tolist()
        Jahr = data_select_inst_ea['PY'].tolist()
        Monat = data_select_inst_ea['PD'].tolist()
        Journal = data_select_inst_ea['SO'].tolist()
        Publisher = data_select_inst_ea['PU'].tolist()
        Disziplin = data_select_inst_ea['SC'].tolist()
        Funding = data_select_inst_ea['FU'].tolist()
        aut_status_ea = []

        Other_Gold = []
        DOAJ_Gold = []
        Green_Accepted = []
        Green_Published = []
        Bronze = []

        ea_li = [Other_Gold, DOAJ_Gold, Green_Accepted, Green_Published, Bronze]

        for oa_status in data_select_inst_ea['OA']:
            aut_status_ea.append('Erstautor')
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

        # Koautoren Listen
        Titel_ka = data_select_inst_ka['TI'].tolist()
        Jahr_ka = data_select_inst_ka['PY'].tolist()
        Monat_ka = data_select_inst_ka['PD'].tolist()
        Journal_ka = data_select_inst_ka['SO'].tolist()
        Publisher_ka = data_select_inst_ka['PU'].tolist()
        Disziplin_ka = data_select_inst_ka['SC'].tolist()
        Funding_ka = data_select_inst_ka['FU'].tolist()
        aut_status_ka = []

        Other_Gold_ka = []
        DOAJ_Gold_ka = []
        Green_Accepted_ka = []
        Green_Published_ka = []
        Bronze_ka = []

        ka_li = [Other_Gold_ka, DOAJ_Gold_ka, Green_Accepted_ka, Green_Published_ka, Bronze_ka]

        for oa_status in data_select_inst_ka['OA']:
            aut_status_ka.append('Koautor')
            if Other_Gold_regex.match(oa_status):
                Other_Gold_ka.append('True')
            else:
                Other_Gold_ka.append('False')
            if DOAJ_Gold_regex.match(oa_status):
                DOAJ_Gold_ka.append('True')
            else:
                DOAJ_Gold_ka.append('False')
            if Green_Accepted_regex.match(oa_status):
                Green_Accepted_ka.append('True')
            else:
                Green_Accepted_ka.append('False')
            if Green_Published_regex.match(oa_status):
                Green_Published_ka.append('True')
            else:
                Green_Published_ka.append('False')
            if Bronze_regex.match(oa_status):
                Bronze_ka.append('True')
            else:
                Bronze_ka.append('False')

        # gemischte Listen:
        mix_titel = Titel + Titel_ka
        mix_Jahr = Jahr + Jahr_ka
        mix_Monat = Monat + Monat_ka
        mix_Journal = Journal + Journal_ka
        mix_Publisher = Publisher + Publisher_ka
        mix_Disziplin = Disziplin + Disziplin_ka
        mix_Funding = Funding + Funding_ka
        mix_aut_status = aut_status_ea + aut_status_ka

        mix_Other_Gold = Other_Gold + Other_Gold_ka
        mix_DOAJ_Gold = DOAJ_Gold + DOAJ_Gold_ka
        mix_Green_Accepted = Green_Accepted + Green_Accepted_ka
        mix_Green_Published = Green_Published + Green_Published_ka
        mix_Bronze = Bronze + Bronze_ka

        mix_li = [mix_Other_Gold, mix_DOAJ_Gold, mix_Green_Accepted, mix_Green_Published, mix_Bronze]

        # Data Frame Build MIX
        main_list_mix = ({
            'Titel': mix_titel,
            'Jahr': mix_Jahr,  # Jahre in INT umwandeln
            'Monat': mix_Monat,
            'Other_Gold': mix_Other_Gold,
            'DOAJ_Gold': mix_DOAJ_Gold,
            'Green_Accepted': mix_Green_Accepted,
            'Green_ Published': mix_Green_Published,
            'Bronze': mix_Bronze,
            'Journal': mix_Journal,
            'Publisher': mix_Publisher,
            'Disziplin': mix_Disziplin,
            'Funding': mix_Funding,
            'Autor-Status': mix_aut_status
        })
        main_list_ea = ({
                'Titel': Titel,
                'Jahr': Jahr, # Jahre in INT umwandeln
                'Monat': Monat,
                'Other_Gold': Other_Gold,
                'DOAJ_Gold': DOAJ_Gold,
                'Green_Accepted': Green_Accepted,
                'Green_ Published': Green_Published,
                'Bronze': Bronze,
                'Journal': Journal,
                'Publisher': Publisher,
                'Disziplin': Disziplin,
                'Funding': Funding,
                'Autor-Status': aut_status_ea
            })

        print(len(Titel), len(Jahr), len(Monat), len(Other_Gold), len(DOAJ_Gold), len(Green_Accepted), len(Green_Published), len(Bronze), len(Journal), len(Publisher), len(Disziplin), len(Funding) )
        dopplung = 0
        for x in Titel:
            for y in Titel_ka:
                if x == y:
                    dopplung += 1
        data_frame = pd.DataFrame(main_list_mix)
# Write Outfile
        if von is None:
            data_frame.to_csv(r'./MAINausgabe.csv')
            print('Outfile erstellt ohne erweiterte Such-Parameter erstellt')
        else:
            gather_Date = (data_frame.loc[(data_frame['Jahr'] >= von) & (data_frame['Jahr'] <= bis)])
            gather_Date.to_csv(r'MAINausgabemitDateSuche.csv')









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
            sizes = len(pie_present(mix_li[0])),\
                    len(pie_present(mix_li[1])),\
                    len(pie_present(mix_li[2])),\
                    len(pie_present(mix_li[3])),\
                    len(pie_present(mix_li[4]))

            colors = ['#f5ff21', '#fffb87', '#4dde93', '#67de4d', '#dea94d']
            plt.rcParams['font.size'] = 6.0
            fig1, ax1 = plt.subplots()

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',startangle=90)

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='darkslategrey')
            fig = plt.gcf()

            plt.title('Open Access Status EA + KA', color='white')

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
            sizes = len(pie_present(ea_li[0])), \
                    len(pie_present(ea_li[1])), \
                    len(pie_present(ea_li[2])), \
                    len(pie_present(ea_li[3])), \
                    len(pie_present(ea_li[4]))

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

            plt.title('Open Access Status Erstautoren', color='white')

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
            sizes = len(pie_present(ka_li[0])), \
                    len(pie_present(ka_li[1])), \
                    len(pie_present(ka_li[2])), \
                    len(pie_present(ka_li[3])), \
                    len(pie_present(ka_li[4]))

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

            plt.title('Open Access Status Koautoren', color='white')

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
        dopp_sum_lbl = Label(center_Frame_left, bg='grey16', fg='white smoke', text='Dopplungen: \n')


        #Result Position LBL:
        ea_sum_lbl.grid(row=0, column=0, sticky='w')
        ka_sum_lbl.grid(row=1, column=0, sticky='w')
        dopp_sum_lbl.grid(row=2, column=0, sticky='w')
    #Chart BTNs:
        pie_chart_mix_btn = Button(center_Frame_left_bottom_one, text=' EA + KA ', command=mix_val_pie)
        pie_chart_ea_btn = Button(center_Frame_left_bottom_one, text='Erstautor ', command=ea_pie)
        pie_chart_ka_btn = Button(center_Frame_left_bottom_one, text=' Koautor  ', command=ka_pie)

    # Chart BTNs Position:
        pie_chart_mix_btn.grid(row=1, column=0, pady=2, sticky='w')
        pie_chart_ea_btn.grid(row=2, column=0, sticky='w')
        pie_chart_ka_btn.grid(row=3, column=0, pady=2,  sticky='w')

    # Results VALUEs
        ea_sum_val = Label(center_Frame_mid,bg='white smoke', fg='black', text=str(len(Titel)))
        ka_sum_val = Label(center_Frame_mid, bg='white smoke', fg='black', text=str(len(Titel_ka)))
        dopp_sum_lbl = Label(center_Frame_mid, bg='white smoke', fg='black', text=str(dopplung))

        pie_desc_lbl = Label(center_Frame_left_bottom_one,bg='grey16', fg='white smoke', text='OA-Status PieCharts:')

        pie_desc_lbl.grid(row=0, column=0, sticky='w')
    # Results VALUEs Position:
        ea_sum_val.grid(row=0, column=0, sticky='w')
        ka_sum_val.grid(row=1, column=0, sticky='w')
        dopp_sum_lbl.grid(row=2, column=0, sticky='w')

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
            sizes = len(pie_present(mix_li[0])),\
                    len(pie_present(mix_li[1])),\
                    len(pie_present(mix_li[2])),\
                    len(pie_present(mix_li[3])),\
                    len(pie_present(mix_li[4]))


            colors = ['#f5ff21', '#fffb87', '#4dde93', '#67de4d', '#dea94d']
            plt.rcParams['font.size'] = 6.0
            fig1, ax1 = plt.subplots()

            patches, texts, autotexts = ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',startangle=90)

            for text in texts:
                text.set_color('white')
            for autotext in autotexts:
                autotext.set_color('white')

            centre_circle = plt.Circle((0, 0), 0.70, fc='darkslategrey')
            fig = plt.gcf()

            plt.title('Open Access Status EA + KA', color='white')

            fig.gca().add_artist(centre_circle)
            fig.patch.set_facecolor('darkslategrey')
            fig.set_size_inches(4, 3)
            ax1.axis('equal')

            #plt.tight_layout()

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