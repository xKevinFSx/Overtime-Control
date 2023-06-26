import tkinter as tk
from tkinter import *
from datetime import date, datetime, timedelta
import calendar
import locale
from tkinter import messagebox
import sqlite3

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Variáveis globais para os campos de entrada
entry_dia = None
entry_hora = None
entry_quantidade_horas = None

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
        
    # Obter o primeiro dia do mês
    primeiro_dia_mes = datetime(ano, mes, 1)

    # Obter o dia da semana do primeiro dia do mês (0 = segunda-feira, 6 = domingo)
    dia_semana_primeiro_dia = primeiro_dia_mes.weekday()

    # Calcular o número de dias no mês anterior
    ultimo_dia_mes_anterior = primeiro_dia_mes - timedelta(days=1)
    num_dias_mes_anterior = ultimo_dia_mes_anterior.day
    
    # Calcular o número de dias no mês atual
    num_dias_mes_atual = calendar.monthrange(ano, mes)[1]

    # Preencher os dias do calendário
    dia_mes_anterior = num_dias_mes_anterior - dia_semana_primeiro_dia + 1
    dia_proximo_mes = 1

    # Preencher os dias do calendário
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            if week_num == 0 and day_num < dia_semana_primeiro_dia:
                # Dias do mês anterior
                label = tk.Label(calendar_frame, text=dia_mes_anterior, padx=10, pady=5, font=('Arial', 35))
                dia_mes_anterior += 1
            elif day == 0:
                # Dias do próximo mês
                label = tk.Label(calendar_frame, text=dia_proximo_mes, padx=10, pady=5, font=('Arial', 35))
                dia_proximo_mes += 1
            elif day > num_dias_mes_atual:
                # Dias adicionais do próximo mês
                label = tk.Label(calendar_frame, text=dia_proximo_mes, padx=10, pady=5, font=('Arial', 35))
                dia_proximo_mes += 1
            else:
                # Dias do mês atual
                label = tk.Label(calendar_frame, text=day, padx=10, pady=5, font=('Arial', 35))
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

# Função para criar a tabela no banco de dados
def criar_tabela():
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS horas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dia TEXT,
                    quantidade_horas INTEGER)''')
    conn.commit()
    conn.close()
    
# Função para converter a data no formato "dd/mm/aaaa" para o formato adequado do SQLite
def converter_data(data):
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    data_sqlite = data_obj.strftime("%Y-%m-%d")
    return data_sqlite
    
# Função para inserir os dados no banco de dados
def inserir_dados():
    dia = entry_dia.get()
    quantidade_horas = entry_quantidade_horas.get()
    
    dia_sqlite = converter_data(dia)
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    c.execute("INSERT INTO horas (dia, quantidade_horas) VALUES (?, ?)", (dia, quantidade_horas))
    conn.commit()
    conn.close()
    
    # Exibir mensagem de sucesso na interface
    mensagem_label.config(text='Horas inseridas com sucesso!')
    

def abrir_config_horas():
    global entry_dia, entry_quantidade_horas, mensagem_label
    
    #Ocultar janela atual
    app.withdraw()
    
    # Criar uma nova janela
    config_window = tk.Toplevel(app)
    config_window.title('Configurar Horas')
    config_window.geometry('1200x700')
    
    # Criar os campos e botão na janela de configuração de horas
    label_dia = tk.Label(config_window, text='Dia:')
    label_dia.grid(row=0, column=0, padx=10, pady=10)
    
    entry_dia = tk.Entry(config_window)
    entry_dia.grid(row=0, column=1, padx=10, pady=10)
    
    label_quantidade_horas = tk.Label(config_window, text='Quantidade de Horas:')
    label_quantidade_horas.grid(row=2, column=0, padx=10, pady=10)
    
    entry_quantidade_horas = tk.Entry(config_window)
    entry_quantidade_horas.grid(row=2, column=1, padx=10, pady=10)
    
    botao_salvar = tk.Button(config_window, text='Salvar', command=inserir_dados)
    botao_salvar.grid(row=3, column=0, columnspan=2, padx=10, pady=10) 
    
    # Label para exibir a mensagem de sucesso
    mensagem_label = tk.Label(config_window, text='')
    mensagem_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
       
    # Função para voltar à janela principal
    def voltar_janela_principal():
        config_window.destroy()
        app.deiconify()  # Mostrar a janela principal novamente
    
    # Criar o menu na janela de configuração de horas
    menubar_config = tk.Menu(config_window)
    config_window.config(menu=menubar_config)
    
    # Criar o item de menu "Voltar"
    menubar_config.add_command(label='VOLTAR ', command=voltar_janela_principal)
    
criar_tabela()
    
#Criar o submenu Configurar Horas    
menu_principal.add_command(label='Configurar Horas', command=abrir_config_horas)

mostrar_calendario()
app.mainloop()
