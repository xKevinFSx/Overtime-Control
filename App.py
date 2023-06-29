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
entry_valor_60 = None
entry_valor_80 = None
entry_valor_100 = None
entry_valor_bip = None
edit_mode = False  # Variável de controle para o modo de edição

valor_60 = None
valor_80 = None
valor_100 = None
valor_bip = None

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
                label = tk.Label(calendar_frame, text=str(dia_mes_anterior).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised')
                dia_mes_anterior += 1
            elif day == 0:
                # Dias do próximo mês
                label = tk.Label(calendar_frame, text=str(dia_proximo_mes).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised')
                dia_proximo_mes += 1
            elif day > num_dias_mes_atual:
                # Dias adicionais do próximo mês
                label = tk.Label(calendar_frame, text=str(dia_proximo_mes).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised')
                dia_proximo_mes += 1
            else:
                # Dias do mês atual
                label = tk.Label(calendar_frame, text=str(day).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised')
            label.grid(row=week_num+1, column=day_num, sticky='w')
    
#Tela
app = tk.Tk()
app.title('Controle de Horas Extras')
app.geometry('1200x700')

# Definir função para atualizar o campo qtd_horas_extras_segsex
def atualizar_qtd_horas_extras():
    # Obter o mês e ano atuais
    hoje = date.today()
    ano = hoje.year
    mes = hoje.month

    # Consultar o banco de dados para obter a quantidade de registros
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM horas WHERE dia_semana IN ('segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira') AND strftime('%Y', data) = ? AND strftime('%m', data) = ?", (ano, mes))
    resultado = c.fetchone()
    conn.close()

    if resultado is not None:
        quantidade = resultado[0]
        qtd_horas_extras_segsex.insert(0, str(quantidade))

#Criar os widgets
header_label = tk.Label(app, text='', font=('Arial', 30, 'bold'))
header_label.grid(row=0, column=0, columnspan=3, padx=140, pady=10, sticky='w')

calendar_frame = tk.Frame(app)
calendar_frame.grid(row=1, column=2, padx=10, pady=10, rowspan=8)

#Criar um campo de label no canto direito
label1 = tk.Label(app, text='Qtd horas extras segunda à sexta: ', font=('Arial', 15, 'bold'))
label1.grid(row=1, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_extras_segsex = tk.Entry(app, text='0', font=('Arial', 15))
qtd_horas_extras_segsex.grid(row=1, column=4, ipadx=0, sticky='sw')

label12 = tk.Label(app, text='Vlr horas extras segunda à sexta: ', font=('Arial', 15, 'bold'))
label12.grid(row=2, column=3, padx=70, sticky='nw')

vlr_horas_extras_segsex = tk.Label(app, text='0', font=('Arial', 15))
vlr_horas_extras_segsex.grid(row=2, column=4,sticky='nw')

label2 = tk.Label(app, text='Qtd horas extras sábado: ', font=('Arial', 15, 'bold'))
label2.grid(row=3, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_extras_sab = tk.Label(app, text='0', font=('Arial', 15))
qtd_horas_extras_sab.grid(row=3, column=4, ipadx=0, sticky='sw')

label21 = tk.Label(app, text='Vlr horas extras sábado: ', font=('Arial', 15, 'bold'))
label21.grid(row=4, column=3, padx=70, pady=0, sticky='nw')

vlr_horas_extras_sab = tk.Label(app, text='0', font=('Arial', 15))
vlr_horas_extras_sab.grid(row=4, column=4,sticky='nw')

label3 = tk.Label(app, text='Qtd horas extras domingo e feriado: ', font=('Arial', 15, 'bold'))
label3.grid(row=5, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_extras_domfer = tk.Label(app, text='0', font=('Arial', 15))
qtd_horas_extras_domfer.grid(row=5, column=4, ipadx=0, sticky='sw')

label31 = tk.Label(app, text='Vlr horas extras domingo e feriado: ', font=('Arial', 15, 'bold'))
label31.grid(row=6, column=3, padx=70, pady=0, sticky='nw')

vlr_horas_extras_domfer = tk.Label(app, text='0', font=('Arial', 15))
vlr_horas_extras_domfer.grid(row=6, column=4,sticky='nw')

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
                    data DATE,
                    quantidade_horas INTEGER,
                    dia_semana TEXT)''')
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
    
    # Verificar se os campos estão preenchidos
    if not dia:
        mensagem_label.config(text='Por favor, preencha um dia!')
        return
    
    if not quantidade_horas:
        mensagem_label.config(text='Por favor, preencha a quantidade de horas!')
        return    
    
    if quantidade_horas == '0':
        mensagem_label.config(text='Por favor, preencha uma quantidade de horas valida!')
        return         
    
    # Obter o dia da semana da data inserida 
    dia_semana = datetime.strptime(dia, '%d/%m/%Y').strftime('%A')
    
    dia_sqlite = converter_data(dia)
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    c.execute("INSERT INTO horas (data, quantidade_horas, dia_semana) VALUES (?, ?, ?)", (dia_sqlite, quantidade_horas, dia_semana))
    conn.commit()
    conn.close()
    
    # Exibir mensagem de sucesso na interface
    mensagem_label.config(text='Horas inseridas com sucesso!')
    
    # Limpar os campos após salvar as horas extras com sucesso
    entry_dia.delete(0, "end")
    entry_quantidade_horas.delete(0, "end")
    
def abrir_config_horas():
    global entry_dia, entry_quantidade_horas, entry_valor_60, entry_valor_80, entry_valor_100, entry_valor_bip, mensagem_label
    
    #Ocultar janela atual
    app.withdraw()
    
    # Criar uma nova janela
    config_window = tk.Toplevel(app)
    config_window.title('Configurar Horas')
    config_window.geometry('1200x700')
    
    # Criar os campos e botão na janela de configuração de horas
    label_titulo1 = tk.Label(config_window, text='Adicionar horas extras', font=('Arial', 16, 'bold'))
    label_titulo1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    label_dia = tk.Label(config_window, text='Dia:')
    label_dia.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    
    entry_dia = tk.Entry(config_window, width=10)
    entry_dia.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    
    label_quantidade_horas = tk.Label(config_window, text='Quantidade de Horas:')
    label_quantidade_horas.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    
    entry_quantidade_horas = tk.Entry(config_window, width=5)
    entry_quantidade_horas.grid(row=2, column=1, padx=10, pady=10, sticky='w')
    
    botao_salvar = tk.Button(config_window, text='Salvar', command=inserir_dados)
    botao_salvar.grid(row=3, column=0, columnspan=2, padx=10, pady=10) 
    
    # Label para exibir a mensagem de sucesso
    mensagem_label = tk.Label(config_window, text='')
    mensagem_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    
    def toggle_edit_mode():
        global edit_mode

        # Inverter o valor da variável de controle
        edit_mode = not edit_mode

        # Habilitar/desabilitar a edição dos campos
        entry_valor_60.config(state='normal' if edit_mode else 'disabled')
        entry_valor_80.config(state='normal' if edit_mode else 'disabled')
        entry_valor_100.config(state='normal' if edit_mode else 'disabled')
        entry_valor_bip.config(state='normal' if edit_mode else 'disabled')
    
    label_titulo2 = tk.Label(config_window, text='Configurar valor de horas extras', font=('Arial', 16, 'bold'))
    label_titulo2.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    
    label_valor_60 = tk.Label(config_window, text='Valor Hora Extra 60%(Segunda a sexta):')
    label_valor_60.grid(row=8, column=0, padx=10, pady=10, sticky='w')
    
    entry_valor_60 = tk.Entry(config_window, width=5, state='normal')
    entry_valor_60.grid(row=8, column=1, padx=10, pady=10, sticky='w')
    entry_valor_60.insert(0, "48.52")
        
    label_valor_80 = tk.Label(config_window, text='Valor Hora Extra 80%(Sabado):')
    label_valor_80.grid(row=9, column=0, padx=10, pady=10, sticky='w')
    
    entry_valor_80 = tk.Entry(config_window, width=5, state='normal')
    entry_valor_80.grid(row=9, column=1, padx=10, pady=10, sticky='w')
    entry_valor_80.insert(0, "54.59")
    
    label_valor_100 = tk.Label(config_window, text='Valor Hora Extra 100%(Domingo e feriado):')
    label_valor_100.grid(row=10, column=0, padx=10, pady=10,  sticky='w')
    
    entry_valor_100 = tk.Entry(config_window, width=5, state='normal')
    entry_valor_100.grid(row=10, column=1, padx=10, pady=10, sticky='w')
    entry_valor_100.insert(0, "60.66")
    
    label_valor_bip = tk.Label(config_window, text='Valor Hora BIP:')
    label_valor_bip.grid(row=11, column=0, padx=10, pady=10,  sticky='w')
    
    entry_valor_bip = tk.Entry(config_window, width=5, state='normal')
    entry_valor_bip.grid(row=11, column=1, padx=10, pady=10, sticky='w')
    entry_valor_bip.insert(0, "10.61")
  
    # Criar o botão para editar os campos
    botao_editar = tk.Button(config_window, text='Editar', command=toggle_edit_mode)
    botao_editar.grid(row=12, column=0, columnspan=2, padx=10, pady=10)    
    
    # Desabilitar os campos
    entry_valor_60.config(state='disabled')
    entry_valor_80.config(state='disabled')
    entry_valor_100.config(state='disabled')
    entry_valor_bip.config(state='disabled')
       
    # Função para voltar à janela principal
    def voltar_janela_principal():
        # Armazenar os valores dos campos
        valor_60 = entry_valor_60.get()
        valor_80 = entry_valor_80.get()
        valor_100 = entry_valor_100.get()
        valor_bip = entry_valor_bip.get()
        
        config_window.destroy()
        app.deiconify()  # Mostrar a janela principal novamente
    
    # Criar o menu na janela de configuração de horas
    menubar_config = tk.Menu(config_window)
    config_window.config(menu=menubar_config)
    
    # Criar o item de menu "Voltar"
    menubar_config.add_command(label='VOLTAR ', command=voltar_janela_principal)
    
    # Configurar o evento para fechar a janela
    config_window.protocol("WM_DELETE_WINDOW", encerrar_programa)
        
def encerrar_programa():
    app.quit()
            
#Criar o submenu Configurar Horas    
menu_principal.add_command(label='Configurar Horas', command=abrir_config_horas)

criar_tabela()
mostrar_calendario()
atualizar_qtd_horas_extras()
app.mainloop()
