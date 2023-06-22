import tkinter as tk
from tkinter import *
from datetime import date
import calendar
import sqlite3

def mostrar_calendario():
    hoje = date.today()
    ano = hoje.year
    mes = hoje.month
    
    #Criar um objeto de calendario
    cal = calendar.monthcalendar(ano, mes)
    
    #Limpar qualquer calendario anterior(se houver)
    if calendar_frame.winfo_children():
        for child in calendar_frame.winfo_children():
            child.destroy()

    #Cabeçalho com o nome do mes e do ano
    header_label.config(text=calendar.month_name[mes] + ' ' + str(ano))
    
    #Preencher os dias da semana acima do calendario
    days_of_week = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    for i, day in enumerate(days_of_week):
        label = tk.Label(calendar_frame, text=day, padx=10, pady=5, font=('Arial', 20, 'bold'))
        label.grid(row=0, column=i)
        
    #Preencher os dias do calendario
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            label = tk.Label(calendar_frame, text=day, padx=10, pady=5, font=('Arial', 35))
            label.grid(row=week_num+1, column=day_num, sticky='w')
    
#tela
app = tk.Tk()
app.title('Controle de Horas Extras')
app.geometry('1000x700')

header_label = tk.Label(app, text='', font=('Arial', 14, 'bold'))
header_label.pack()

calendar_frame = tk.Frame(app)
calendar_frame.pack(side='left', padx=10, pady=10)

#Criar a menu bar
menubar = Menu(app)
app.config(menu=menubar)
        
#Criar itens do menu
menubar.add_command(label='INICIO')
menubar.add_command(label='CONFIG HORAS')
menubar.add_command(label='SAIR', command=app.quit)


mostrar_calendario()
app.mainloop()

    #Crie uma conexão com o banco de dados SQLite
    #self.coon = sqlite3.connect('overtime.db')
    #self.cursor = self.coon.cursor()

    #Crie a tabela se ela não existir
    #self.cursor.execute('''CREATE TABLE IF NOT EXISTS horas_extras (
    #    id INTEGER PRIMARY KEY AUTOINCREMENT,
    #    data TEXT,
    #    horas_bip REAL,
    #    horas_exts REAL
    #)''')
        
    #Criar menu superior
        
