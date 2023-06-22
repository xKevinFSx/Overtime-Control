import tkinter as tk
from tkinter import *
from datetime import date
import calendar
import locale
from tkinter import messagebox
import sqlite3

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
    mes_nome = calendar.month_name[mes].capitalize()
    header_label.config(text=f'{mes_nome} de {ano}')
    #header_label.config(text=calendar.month_name[mes] + ' de ' + str(ano))
    
    #Preencher os dias da semana acima do calendario
    days_of_week = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    for i, day in enumerate(days_of_week):
        label = tk.Label(calendar_frame, text=day, padx=10, pady=5, font=('Arial', 20, 'bold'))
        label.grid(row=0, column=i)
        
    #Preencher os dias do calendario
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            label = tk.Label(calendar_frame, text=day, padx=10, pady=5, font=('Arial', 30))
            label.grid(row=week_num+1, column=day_num, sticky='w')
    
#Tela
app = tk.Tk()
app.title('Controle de Horas Extras')
app.geometry('1200x700')

#Criar os widgets
header_label = tk.Label(app, text='', font=('Arial', 30, 'bold'))
header_label.grid(row=0, column=0, columnspan=3, padx=140, pady=10, sticky='w')

calendar_frame = tk.Frame(app)
calendar_frame.grid(row=1, column=2, padx=10, pady=10, rowspan=8)

#Criar um campo de label no canto direito
label1 = tk.Label(app, text='Qtd horas extras segunda à sexta: ', font=('Arial', 15, 'bold'))
label1.grid(row=1, column=3, padx=70, pady=0, sticky='sw')

label12 = tk.Label(app, text='Vlr horas extras segunda à sexta: ', font=('Arial', 15, 'bold'))
label12.grid(row=2, column=3, padx=70, sticky='nw')

label2 = tk.Label(app, text='Qtd horas extras sábado: ', font=('Arial', 15, 'bold'))
label2.grid(row=3, column=3, padx=70, pady=0, sticky='sw')

label21 = tk.Label(app, text='Vlr horas extras sábado: ', font=('Arial', 15, 'bold'))
label21.grid(row=4, column=3, padx=70, pady=0, sticky='nw')

label3 = tk.Label(app, text='Qtd horas extras domingo e feriado: ', font=('Arial', 15, 'bold'))
label3.grid(row=5, column=3, padx=70, pady=0, sticky='sw')

label31 = tk.Label(app, text='Vlr horas extras domingo e feriado: ', font=('Arial', 15, 'bold'))
label31.grid(row=6, column=3, padx=70, pady=0, sticky='nw')

#Criar a menu bar
menubar = Menu(app)
app.config(menu=menubar)

#Criar o menu
menu_principal = tk.Menu(menubar, tearoff=0)
        
#Criar itens do menu
menubar.add_cascade(label='MENU', menu=menu_principal)
menubar.add_command(label='SAIR', command=app.quit)

def abrir_config_horas():
    #Ocultar janela atual
    app.withdraw()
    
    # Criar uma nova janela
    config_window = tk.Toplevel(app)
    config_window.title('Configurar Horas')
    config_window.geometry('1200x700')    
    
    # Função para voltar à janela principal
    def voltar_janela_principal():
        config_window.destroy()
        app.deiconify()  # Mostrar a janela principal novamente
    
    # Criar o menu na janela de configuração de horas
    menubar_config = tk.Menu(config_window)
    config_window.config(menu=menubar_config)
    
    # Criar o item de menu "Voltar"
    menubar_config.add_command(label='VOLTAR ', command=voltar_janela_principal)
    
#Criar o submenu Configurar Horas    
menu_principal.add_command(label='Configurar Horas', command=abrir_config_horas)

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
        
