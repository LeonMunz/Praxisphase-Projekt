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






def startwindow():
    def close_window():
        window.destroy()
    #Functionen der GUI
    def mainWindowGrey():
        # Funktionen des Scripts:
        '''
        Die Funktion "selectDir" ermöglicht das Festlegen, via grafischer Oberfläche, eines Speicherorts der zu
        analysierenden BibTex-Files.
        '''

        def selectDir():
            sdir = filedialog.askdirectory()
            dir_lbl.configure(text=sdir, fg='green2')
            weiterbtn.configure(text='   Weiter   ', bg='white', fg='black', command=secondWindowblue)

            for filename in glob.glob(os.path.join(sdir, '*.bib')):
                print('Dateien werden zusammengeführt')
                with open(filename, 'r') as f:
                    with open('./Zusammengeführte_BibTex_Files/collection.bib', 'a') as outfile:
                        for line in f:
                            outfile.write(line)
            print('collection_File_erstelllt')


        def selectDir_result():
            global sdir_res
            sdir_res = filedialog.askdirectory()
            dir_lbl_res.configure(text=sdir_res, fg='green2')
            return sdir_res

        # Kontroll Funktionen
        def kontrol_dir():
            dir_lbl.configure(text='Bitte wählen Sie zu erst ein Verzeichnis.', fg='red')




        #Display_Frames

        center_Frame0 = Frame(window, width=700, height=550, bg='grey19')

        center_space_Frame_top = Frame(window, width=900, height=80, highlightbackground="grey19",
                                       highlightthickness=1, bg='grey16')
        center_space_Frame_left = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_rigth = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_center = Frame(center_Frame0, width= 600, height=380, bg='grey16')
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20",
                             highlightthickness=1, bg='grey16')

        bottom_space_Frame_left = Frame(bottom_Frame, width=532, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=100, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        #Positioning_Frames
        center_Frame0.grid_rowconfigure(0, weight=1)
        center_Frame0.grid_columnconfigure(1, weight=1)

        center_Frame0.grid(row=1, column=0, sticky='nsew')

        center_space_Frame_top.grid(row=0, column=0, sticky='ew')
        center_space_Frame_left.grid(row=0, column=0, sticky='ns')
        center_space_Frame_rigth.grid(row=0, column=2, sticky='ns')
        center_space_Frame_center.grid(row=0, column=1, sticky='nsew')
        bottom_Frame.grid(column=0, row=2, sticky='esw')

        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')

        #BTNS
        weiterbtn = Button(bottom_button_Frame_forw, bg='grey17', fg='gray33', text='   Weiter   ', command=kontrol_dir)

        #BTNS Position
        weiterbtn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')

        #CONTENT
        #img

        #--center
        wel_lbl = Label(center_space_Frame_center, fg='white smoke', bg='grey16', justify=LEFT, text=
        'Hier steht ein Blindtext in voller Länge                                          \n'
        'Dieser Text wird noch erweitert und soll einige Erläuterungen zum Programm enthalten\n'
        'Dieser Text wird noch erweitert und soll einige Erläuterungen zum Programm enthalten\n'
        'Dieser Text wird noch erweitert und soll einige Erläuterungen zum Programm enthalten\n'
        )

        instruction_lbl = Label(center_space_Frame_center, fg='white smoke', bg='grey16', justify=LEFT, text=
        ' \n'
        'Bitte wählen Sie das Verzeichnis in dem sich die einzelnen BibTex-Files befinden: \n'
        ' ')

        result_dir_lbl =Label(center_space_Frame_center, fg='white smoke', bg='grey16', justify=LEFT, text=
        '\n'
        '\n'
        'Bitte wählen Sie das Verzeichnis in dem die Ergebnisfiles abgelegt werden sollen:'
        '\n'
        '*Falls keine Auswahl getroffen wird, werden die Files im Programmordner abgelegt'
        '\n')


        dir_lbl = Label(center_space_Frame_center, text=' ', fg='green2', bg='grey16')
        dir_lbl_res = Label(center_space_Frame_center, text=' ', fg='green2', bg='grey16')

        #--center BTNS
        dir_btn = Button(center_space_Frame_center, text='Verzeichnis wählen', command=selectDir)
        dir_btn_result = Button(center_space_Frame_center, text='Verzeichnis wählen', command=selectDir_result)

        #Positioning Content
        #--top

        #--center
        wel_lbl.grid(row=0, column=0, sticky='n')

        instruction_lbl.grid(row=1, column=0, sticky='w')
        result_dir_lbl.grid(row=3, column=0, sticky='w')
        dir_lbl.grid(row=2, column=1, sticky='w')
        dir_lbl_res.grid(row=4, column=1, sticky='w')

        dir_btn.grid(row=2, column=0, sticky='w')
        dir_btn_result.grid(row=4, column=0, sticky='w')



    def secondWindowblue():
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
#-----------------------------------AUSLESEN DER DATEN UND DAZUGEHÖRIGE FUNKTIONEN-------------------------------------#
        def start():
            with open('./Zusammengeführte_BibTex_Files/collection.bib') as bibtex_file:
                bibtex_str = bibtex_file.read()

            bib_database = bibtexparser.loads(bibtex_str)

            Erstautoren_regex = re.compile(r'.*%s.*' % sb()[0], re.IGNORECASE)
            Koautoren_regex = re.compile(r'.*\s\(Reprint\sAuthor\).*%s.*\.' % sb()[1], re.IGNORECASE)
            print('Autoren werden gefiltert.')

            # VARIABLEN
            global countStatus
            global Titel
            global autor_status_count
            global Journals
            global re_area
            global Publisher
            global oastatus

            Autoren_Collection = []
            Autoren_Status = []

            oastatus = []
            Titel = []

            Year = []
            Month = []
            Monthtranslate = []
            Journals = []
            re_area = []
            Publisher = []
            FA = []
            Namen = []

            attribute_result = [
                Titel,
                Autoren_Status,
                oastatus,
                Year,
                Monthtranslate,
                Journals,
                re_area,
                Publisher,
                FA,
                Namen
            ]

            MoNu = [(1, 'JAN'), (2, 'FEB'),
                    (3, 'MÄR'), (4, 'APR'),
                    (5, 'MAY'), (6, 'JUN'),
                    (7, 'JUL'), (8, 'AUG'),
                    (9, 'SEP'), (10, 'OKT'),
                    (11, 'NOV'), (12, 'DEZ')]

            for aut in bib_database.entries:
                oa = aut.get('oa')
                if oa is not None:  # prüfen ob OA-Status vorhanden ist, wenn nein wird der Eintrag übersprungen
                    add = aut.get('address')
                    add2 = aut.get('affiliation')
                    if Erstautoren_regex.match(add):
                        if aut not in Autoren_Collection:  # Doubletten Kontrolle
                            Autoren_Collection.append(aut)
                            Autoren_Status.append('Erstautor: ' + '(' + sb()[0] + ')')
                    if Koautoren_regex.match(add2):
                        Autoren_Collection.append(aut)
                        Autoren_Status.append('Reprint-Autor: ' + '(' + sb()[1] + ')')

            for oa in Autoren_Collection:
                add = oa.get('oa')
                q = add.replace('{', '')
                z = q.replace('}', '')
                oastatus.append(z)

            for tit in Autoren_Collection:
                add = tit.get('title')
                if add is not None:
                    q = add.replace('{', '')
                    z = q.replace('}', '')
                    y = z.replace('\n', '')
                    Titel.append(y)

            for tim in Autoren_Collection:
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
            for l in Month:
                for x in MoNu:
                    if x[1] == l:
                        v = l.replace(l, str(x[0]))
                        Monthtranslate.append(v)

            for jour in Autoren_Collection:
                add = jour.get('journal')
                if add is not None:
                    q = add.replace('{', '')
                    z = q.replace('}', '')
                    Journals.append(z)

            for ra in Autoren_Collection:
                add = ra.get('research-areas')
                if add is not None:
                    q = add.replace('{', '')
                    z = q.replace('}', '')
                    re_area.append(z)

            for pub in Autoren_Collection:
                add = pub.get('publisher')
                if add is not None:
                    q = add.replace('{', '')
                    z = q.replace('}', '')
                    Publisher.append(z)

            for funding in Autoren_Collection:
                add = funding.get('funding-acknowledgement')
                if add is not None:
                    a = add.replace('{', '')
                    b = a.replace('}', '')
                    c = b.replace('\n', '')
                    d = c.replace('\\', '')
                    FA.append(d)

            for nam in Autoren_Collection:
                add = nam.get('author')
                a = add.replace('{', '')
                b = a.replace('}', '')
                c = b.replace('and', '')
                d = c.replace('\n', '')
                Namen.append(d)

            z = 0
            counter = []
            for x in Autoren_Status:
                x = Autoren_Status.count(Autoren_Status[z])
                z += 1
                counter.append(x)
                countStatus = dict(zip(Autoren_Status, counter))
            autor_status_count = []
            for i in countStatus.values():
                autor_status_count.append(i)

            export_data = zip_longest(*attribute_result, fillvalue='')

            try:
                sdir_comb = sdir_res + '/resultfromsdirres.csv'
                with open(sdir_comb, 'w', encoding="ISO-8859-1", newline='') as out:
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
            except:
                with open('resultlolololol.csv', 'w', encoding="ISO-8859-1", newline='') as out:
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
            os.remove('./Zusammengeführte_BibTex_Files/collection.bib')
            print('Collection-File gelöscht')
            print('Result-CSV Erstellt')
            thirdwindow()
            return Titel, Autoren_Status


#----------------------------------------------------------------------------------------------------------------------#
        #Display_Frames

        center_Frame0 = Frame(window, width=800, height=550, bg='grey19')
        #content_Frame = Frame(center_Frame0, width=300, height=200, bg='green')


        center_space_Frame_top = Frame(window, width=900, height=80, highlightbackground="grey20", highlightthickness=1, bg='grey16')
        center_space_Frame_left = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_rigth = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_center = Frame(center_Frame0, width= 600, height=380, bg='grey16')
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20", highlightthickness=1, bg='grey16')


        bottom_space_Frame_left = Frame(bottom_Frame, width=562, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=100, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        #Positioning_Frames
        center_Frame0.grid_rowconfigure(0, weight=1)
        center_Frame0.grid_columnconfigure(1, weight=1)


        center_Frame0.grid(row=1, column=0, sticky='nsew')
        #content_Frame.grid(row=1, column=0, sticky='nwse')

        center_space_Frame_left.grid(row=0, column=0, sticky='ns')
        center_space_Frame_top.grid(row=0, column=0, sticky='ew')
        center_space_Frame_rigth.grid(row=0, column=2, sticky='ns')
        center_space_Frame_center.grid(row=0, column=1, sticky='nsew')


        bottom_Frame.grid(column=0, row=2, sticky='esw')

        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')

        #BTNS
        weiterbtn = Button(bottom_button_Frame_forw, text='   Weiter   ', command=start)
        back_btn = Button(bottom_button_Frame_back, text='   Zurück   ', command=mainWindowGrey)
        choose_btn = Button(center_space_Frame_center, text='  Eingabe Bestätigen  ', command=sb)

        #BTNS Position
        weiterbtn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')
        back_btn.grid(column=0, row=0,  padx=2, pady=5, sticky='nwse')
        choose_btn.grid(row=4, column=1, pady=20, sticky='w')

        #CONTENT
        wel_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', justify=LEFT, text=
        'Hier kommt ein angenehm inhaltsschwangerer, informativer Text zum Einsatz\n'
        'Dieser muss nur noch von der entsprechenden Person verfasst werden.\n\n')

        nfo_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', text=
        'Eingabe der zu suchenden Institutionen:\n\n\n')

        entry_ea_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', justify=LEFT, text=
        'Institution Erstautor:')
        entry_ko_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', justify=LEFT, text=
        'Institution Koautor:')

        entry_ea_choice_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', justify=LEFT, text=' ')
        entry_ko_choice_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', justify=LEFT, text=' ')

        entry_ea = Entry(center_space_Frame_center, width=20)
        entry_ko = Entry(center_space_Frame_center, width=20)

        #Positioning Content
        wel_lbl.grid(row=0, columnspan=3, sticky='w')
        nfo_lbl.grid(row=1, column=0, sticky='w')

        entry_ea_lbl.grid(row=2, column=0, sticky='we')
        entry_ko_lbl.grid(row=3, column=0, sticky='we')

        entry_ea_choice_lbl.grid(row=2, column=2, padx=10, sticky='w')
        entry_ko_choice_lbl.grid(row=3, column=2, padx=10, sticky='w')

        entry_ea.grid(row=2, column=1, pady=20, sticky='w')
        entry_ko.grid(row=3, column=1, sticky='w')


    def thirdwindow():
        #Funktionen zur Ausgabe innerhalb der GUI (im dritten Fenster)
        def Listen_Ranking(v):
            z = 0
            counter = []
            for x in v:
                x = v.count(v[z])
                z += 1
                counter.append(x)
                dictionary = dict(zip(v, counter))
            return (dictionary)

        max_oa_status = max(Listen_Ranking(oastatus), key=Listen_Ranking(oastatus).get)

        def printinGUI(a):
            for i in a.values():
                if i == 1:
                    message = 'Ausgeglichen'
                    print(message)
                else:
                    max_key = max(a, key=a.get)
                    message = str(max_key)
                    print(message)
            return message




            # Display_Frames
        center_Frame0 = Frame(window, width=800, height=550, bg='grey19')
            # content_Frame = Frame(center_Frame0, width=300, height=200, bg='green')

        center_space_Frame_top = Frame(window, width=900, height=80, highlightbackground="grey20", highlightthickness=1,
                                           bg='grey16')
        center_space_Frame_left = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_rigth = Frame(center_Frame0, width=100, height=380, bg='grey16')
        center_space_Frame_center = Frame(center_Frame0, width=600, height=380, bg='grey16')
        bottom_Frame = Frame(window, width=800, height=100, highlightbackground="grey20", highlightthickness=1,
                                 bg='grey16')

        bottom_space_Frame_left = Frame(bottom_Frame, width=562, height=100, bg='grey16')
        bottom_space_Frame_rigth = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        bottom_button_Frame_back = Frame(bottom_Frame, width=100, height=100, bg='grey16')
        bottom_button_Frame_forw = Frame(bottom_Frame, width=100, height=100, bg='grey16')

        # Positioning_Frames
        center_Frame0.grid_rowconfigure(0, weight=1)
        center_Frame0.grid_columnconfigure(1, weight=1)

        center_Frame0.grid(row=1, column=0, sticky='nsew')
             # content_Frame.grid(row=1, column=0, sticky='nwse')

        center_space_Frame_left.grid(row=0, column=0, sticky='ns')
        center_space_Frame_top.grid(row=0, column=0, sticky='ew')
        center_space_Frame_rigth.grid(row=0, column=2, sticky='ns')
        center_space_Frame_center.grid(row=0, column=1, sticky='nsew')

        bottom_Frame.grid(column=0, row=2, sticky='esw')

        bottom_space_Frame_left.grid(row=0, column=0, sticky='w')
        bottom_space_Frame_rigth.grid(row=0, column=3, sticky='e')

        bottom_button_Frame_back.grid(row=0, column=1, sticky='e')
        bottom_button_Frame_forw.grid(row=0, column=2, sticky='e')

            # BTNS
        weiterbtn = Button(bottom_button_Frame_forw, text='   Programm schließen   ', command= close_window)
        back_btn = Button(bottom_button_Frame_back, text='   Zurück   ', command=secondWindowblue)


            # BTNS Position
        weiterbtn.grid(column=0, row=0, padx=2, pady=5, sticky='nwse')
        back_btn.grid(column=0, row=0,  padx=2, pady=5, sticky='nwse')


            # CONTENT
        wel_lbl = Label(center_space_Frame_center, bg='grey16', fg='white smoke', justify=LEFT, text=
            'Ergebnisliste: \n'
            '\n\n')

        resul_lbl = Label(center_space_Frame_center, bg='white smoke', fg='black', justify=LEFT, text=
        'Insgesamt gefundene Einträge:     ' + '   \n\n'
        'Erstautoren Einträge: ' + '(' + ea + ')' + '\n' +
        'Koautoren Einträge: ' + '(' + ka + ')' + '\n' +
        'Journals:' + '\n' +
        'Publisher:' + '\n' +
        'Disziplinen:'
                          )



        oa_status_lbl = Label(center_space_Frame_center, bg='white smoke', fg='black', justify=LEFT, text= 'Häufigster OA-Status: ' + '\n' + 'Häufigstes Journal: ' + '\n' + 'Häufigster Publisher')
        oa_status_lbl_numb = Label(center_space_Frame_center, bg='white smoke', fg='black', justify=LEFT, text= printinGUI(Listen_Ranking(oastatus)) + '\n' + printinGUI(Listen_Ranking(Journals)) + '\n' + printinGUI(Listen_Ranking(Publisher)))

        #journal_lbl = Label(center_space_Frame_center, bg='white smoke', fg='black', justify=LEFT,text='Häufigstes Journal: ')






        resul_numb_lbl_left = Label(center_space_Frame_center, bg='white smoke', fg='black', justify=LEFT, text=str(len(Titel)) + '\n\n' + str(autor_status_count[0]) + '\n' + str(autor_status_count[1]) + '\n' + str(len(Journals)) + '\n' + (str(len(Publisher))) + '\n' + (str(len(re_area))))

        #resul_numb_lbl_rigth = Label(center_space_Frame_center, bg='white smoke', fg='black', justify=LEFT, text='')
        



        #print(getlist(Listen_Ranking(oastatus))[0])
        #print(getlist(Listen_Ranking(oastatus))[1])



        # Positioning Content
        wel_lbl.grid(row=0, columnspan=3, sticky='w')
        resul_lbl.grid(row=1, column=0, sticky='w')
        resul_numb_lbl_left.grid(row=1, column=1, sticky='w')
        #resul_numb_lbl_rigth.grid(row=1, column=2, sticky='w')

        oa_status_lbl.grid(row=1, column=3, sticky='nw')
        oa_status_lbl_numb.grid(row=1, column=4, sticky='nw')
        #journal_lbl.grid(row=1, column=3, sticky='nw')








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


    mainWindowGrey()
    #thirdwindow()


    window.mainloop()

startwindow()