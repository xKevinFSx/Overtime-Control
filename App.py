import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import date, datetime, timedelta
import calendar
import locale
import sqlite3
from tkcalendar import DateEntry

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Variáveis globais para os campos de entrada
hoje = date.today()
mes = hoje.month
ano = hoje.year

mes_anterior = mes - 1

#Adicionar zeros a esquerda do hoje e do mes quando necessairo
mes_formatado = str(mes).zfill(2)
mes_anterior_formatado = str(mes_anterior).zfill(2)

entry_dia = None
entry_hora = None
entry_quantidade_horas = None
entry_valor_60 = None
entry_valor_80 = None
entry_valor_100 = None
entry_valor_bip = None
edit_mode = False  # Variável de controle para o modo de edição

valor_60 = 48.52
valor_80 = 54.59
valor_100 = 60.66
valor_bip = 10.61

total_horas_semana = 0
total_horas_sabado = 0
total_horas_domingo = 0
total_horas_bip = 0

def mostrar_calendario():
    global hoje, mes, mes_anterior, resultado5
    
    #Criar um objeto de calendario
    calendar.setfirstweekday(calendar.SUNDAY)
    cal = calendar.monthcalendar(ano, mes)
    
    #Limpar qualquer calendario anterior(se houver)
    if calendar_frame.winfo_children():
        for child in calendar_frame.winfo_children():
            child.destroy()

    #Cabeçalho com o nome do mes e do ano
    mes_nome = calendar.month_name[mes].capitalize()
    header_label.config(text=f'{mes_nome} de {ano}')
    
    #Preencher os dias da semana acima do calendario
    days_of_week = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']
    for i, day in enumerate(days_of_week):
        label = tk.Label(calendar_frame, text=day, padx=10, pady=5, font=('Arial', 20, 'bold'))
        label.grid(row=0, column=i)
        
    #Obter o primeiro dia do mês
    primeiro_dia_mes = datetime(ano, mes, 1)

    #Obter o dia da semana do primeiro dia do mês (0 = domingo, 6 = sabado)
    dia_semana_primeiro_dia = primeiro_dia_mes.weekday()

    #Calcular o número de dias no mês anterior
    ultimo_dia_mes_anterior = primeiro_dia_mes - timedelta(days=1)
    num_dias_mes_anterior = ultimo_dia_mes_anterior.day
    mes_anterior = mes - 1
    
    #Calcular o número de dias no mês atual
    num_dias_mes_atual = calendar.monthrange(ano, mes)[1]

    #Preencher os dias do calendário
    dia_mes_anterior = num_dias_mes_anterior - dia_semana_primeiro_dia 
    dia_proximo_mes = 1
    
    #Resgatar os resultados da consulta no banco de dados
    datas_plantao = []
    for data_inicio, data_fim in resultado5:
        dia_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        dia_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        datas_plantao.append((dia_inicio, dia_fim))

    #Preencher os dias do calendário
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            if week_num == 0 and day_num <= dia_semana_primeiro_dia:
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
                data_obj = datetime(ano, mes, day).date()
                for dia_inicio, dia_fim in datas_plantao:
                    if dia_inicio <= data_obj <= dia_fim:
                        label = tk.Label(calendar_frame, text=str(day).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised', bg='purple')
                        break
                    else:
                        label = tk.Label(calendar_frame, text=str(day).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised')
            label.grid(row=week_num+1, column=day_num, sticky='e')
    
#Tela
app = tk.Tk()
app.title('Controle de Horas Extras')
app.resizable(False, False)
app.geometry('1200x700')

# Definir função para atualizar o campo qtd_horas_extras_segsex
def atualizar_qtd_horas_extras():
    global total_horas_semana, total_horas_sabado, total_horas_domingo, total_horas_bip, hoje, mes, ano, mes_anterior, resultado5
    
    #limpar as variaveis de horas
    total_horas_semana = 0
    total_horas_sabado = 0
    total_horas_domingo = 0
    total_horas_bip = 0
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    
    #Range de datas do dia 16 do ultimo mês até dia 15 do mês atual
    data_mes_anterior = str(ano) + '-' + mes_anterior_formatado + '-' + '16'
    data_mes_atual = str(ano) + '-' + mes_formatado + '-' + '15'
    
    dias_semana = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
    
    #Contar qtd de horas extras na semana
    for dia_semana in dias_semana:
        consulta1 = f"SELECT SUM(quantidade_horas) FROM horas WHERE dia_semana = ? AND data BETWEEN  ? AND  ?"
        c.execute(consulta1, (dia_semana, data_mes_anterior, data_mes_atual))
        
        resultado1 = c.fetchone()
        if resultado1 [0]:
            total_horas_semana += resultado1[0]
            
    #Contar qtd de horas extras nos sabados
    consulta2 = "SELECT SUM(quantidade_horas) FROM horas WHERE dia_semana = 'sábado' AND data BETWEEN ? AND ?"        
    c.execute(consulta2, (data_mes_anterior, data_mes_atual))
    
    resultado2 = c.fetchone()
    if resultado2[0]:
        total_horas_sabado += resultado2[0]
            
    #Contar qtd de horas extras nos sabados
    consulta3 = "SELECT SUM(quantidade_horas) FROM horas WHERE dia_semana = 'domingo' AND data BETWEEN ? AND ?"        
    c.execute(consulta3, (data_mes_anterior, data_mes_atual))
    
    resultado3 = c.fetchone()
    if resultado3[0]:
        total_horas_domingo += resultado3[0]      
    
    #Contar qtd de horas BIPs no mês
    consulta4 = "SELECT SUM(quantidade_horas) FROM horas_bip WHERE data_fim BETWEEN ? AND ?"
    c.execute(consulta4, (data_mes_anterior, data_mes_atual))
    
    resultado4 = c.fetchone()
    if resultado4[0]:
        total_horas_bip += resultado4[0]      

    #Selecionar datas de plantãp
    consulta5 = "SELECT data_inicio, data_fim FROM plantao_hrs"
    c.execute(consulta5)
    
    resultado5 = c.fetchall()
    conn.close()
    
    qtd_horas_extras_segsex.config(text=f"{total_horas_semana} hora(s)")
    qtd_horas_extras_sab.config(text=f"{total_horas_sabado} hora(s)")
    qtd_horas_extras_domfer.config(text=f"{total_horas_domingo} hora(s)")
    qtd_horas_bips.config(text=f'{total_horas_bip} hora(s)')
    
    if valor_60 is not None:
        resultado_segsex = total_horas_semana * valor_60
        resultado_segsex_str = str(resultado_segsex).replace('.', ',')
        vlr_horas_extras_segsex.config(text=f"R$ {resultado_segsex_str}")
    else:
        None
    
    if valor_80 is not None:
        resultado_sab = total_horas_sabado * valor_80
        resultado_sab_str = str(resultado_sab).replace('.', ',')
        vlr_horas_extras_sab.config(text=f"R$ {resultado_sab_str}")
    else:
        None
        
    if valor_100 is not None:
        resultado_dom = total_horas_domingo * valor_100
        resultado_dom_str = str(resultado_dom).replace('.', ',')
        vlr_horas_extras_domfer.config(text=f"R$ {resultado_dom_str}")
    else:
        None
        
    if valor_bip is not None:
        resultado_bip = total_horas_bip * valor_bip
        resultado_bip_str = str(resultado_bip).replace('.', ',')
        vlr_horas_bips.config(text=f"R$ {resultado_bip_str}")
    else:
        None
        
#Criar os widgets
header_label = tk.Label(app, text='', font=('Arial', 30, 'bold'))
header_label.grid(row=0, column=0, columnspan=3, padx=140, pady=10, sticky='w')

calendar_frame = tk.Frame(app)
calendar_frame.grid(row=1, column=2, padx=10, pady=10, rowspan=8)

label_titulo = tk.Label(app, text=f'Valores calculados do dia 16/0{mes_anterior} até o dia 15/0{mes}', font=('Arial', 18, 'bold'))
label_titulo.grid(row=0, column=3, columnspan=2, sticky='w')

#Criar um campo de label no canto direito
label1 = tk.Label(app, text='Qtd horas extras segunda à sexta:', font=('Arial', 15, 'bold'))
label1.grid(row=1, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_extras_segsex = tk.Label(app, font=('Arial', 15))
qtd_horas_extras_segsex.grid(row=1, column=3, columnspan=2, padx=410, sticky='sw')

label12 = tk.Label(app, text='Vlr horas extras segunda à sexta:', font=('Arial', 15, 'bold'))
label12.grid(row=2, column=3, padx=70, sticky='nw')

vlr_horas_extras_segsex = tk.Label(app, font=('Arial', 15))
vlr_horas_extras_segsex.grid(row=2, column=3, columnspan=2, padx=410, sticky='nw')

label2 = tk.Label(app, text='Qtd horas extras sábado:', font=('Arial', 15, 'bold'))
label2.grid(row=3, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_extras_sab = tk.Label(app, font=('Arial', 15))
qtd_horas_extras_sab.grid(row=3, column=3, columnspan=2, padx=325, sticky='sw')

label21 = tk.Label(app, text='Vlr horas extras sábado:', font=('Arial', 15, 'bold'))
label21.grid(row=4, column=3, padx=70, pady=0, sticky='nw')

vlr_horas_extras_sab = tk.Label(app, font=('Arial', 15))
vlr_horas_extras_sab.grid(row=4, column=3, columnspan=2, padx=325, sticky='nw')

label3 = tk.Label(app, text='Qtd horas extras domingo e feriado:', font=('Arial', 15, 'bold'))
label3.grid(row=5, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_extras_domfer = tk.Label(app, font=('Arial', 15))
qtd_horas_extras_domfer.grid(row=5, column=3, columnspan=2, padx=425, sticky='sw')

label31 = tk.Label(app, text='Vlr horas extras domingo e feriado:', font=('Arial', 15, 'bold'))
label31.grid(row=6, column=3, padx=70, pady=0, sticky='nw')

vlr_horas_extras_domfer = tk.Label(app, font=('Arial', 15))
vlr_horas_extras_domfer.grid(row=6, column=3, columnspan=2, padx=425, sticky='nw')

label4 = tk.Label(app, text='Qtd horas BIPs:', font=('Arial', 15, 'bold'))
label4.grid(row=7, column=3, padx=70, pady=0, sticky='sw')

qtd_horas_bips = tk.Label(app, font=('Arial', 15))
qtd_horas_bips.grid(row=7, column=3, columnspan=2, padx=230, sticky='sw')

label41 = tk.Label(app, text='Vlr horas BIPs:', font=('Arial', 15, 'bold'))
label41.grid(row=8, column=3, padx=70, pady=0, sticky='nw')

vlr_horas_bips = tk.Label(app, font=('Arial', 15))
vlr_horas_bips.grid(row=8, column=3, columnspan=2, padx=230, sticky='nw')

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
    
    c.execute('''CREATE TABLE IF NOT EXISTS horas_bip (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_fim DATE,
                    quantidade_horas INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS plantao_hrs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_inicio DATE,
                    data_fim DATE)''')
    conn.commit()
    conn.close()
    
# Função para converter a data no formato "dd/mm/aaaa" para o formato adequado do SQLite
def converter_data(data):
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    data_sqlite = data_obj.strftime("%Y-%m-%d")
    return data_sqlite
    
# Função para inserir horas extras no banco de dados
def inserir_horas_extra():
    dia = cal_dia_hora_extra.get()
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
    cal_dia_hora_extra.delete(0, "end")
    entry_quantidade_horas.delete(0, "end")
    
    #Chamar função para limpar mensagem de sucesso ou falha
    config_window.after(5000, lambda: mensagem_label.config(text=''))
    
#Função para inserir horas BIP no banco de dados
def inserir_horas_bip():
    data_quinzena = cal_quinzena.get()
    horas_bip = entry_horas_bip.get()
    
    #Verificar se os campos estão preenchidos   
    if not data_quinzena:
        mensagem_label2.config(text='Por favor, preencha uma data!')
        return    
    
    if horas_bip == '0':
        mensagem_label2.config(text='Por favor, preencha uma quantidade de horas valida!')
        return         
    
    data_bip = converter_data(data_quinzena)
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    c.execute("INSERT INTO horas_bip (data_fim, quantidade_horas) VALUES (?, ?)", (data_bip, horas_bip))
    conn.commit()
    conn.close()
    
    #Exibir mensagem de sucesso na interface
    mensagem_label2.config(text='Horas BIP inseridas com sucesso!')
    
    #Limpar os campos após salvar as horas extras com sucesso
    cal_quinzena.delete(0, "end")
    entry_horas_bip.delete(0, "end")
    
    #Chamar função para limpar mensagem de sucesso ou falha
    config_window.after(5000, lambda: mensagem_label2.config(text=''))

def inserir_datas_plantao():
    data_ini_plantao = cal_inicio.get()
    data_fim_plantao = cal_fim.get()
    
    #Verificar se os campos estão preenchidos   
    if not data_ini_plantao:
        mensagem_label3.config(text='Por favor, preencha uma data inicio!')
        return 
    
    if not data_fim_plantao:
        mensagem_label3.config(text='Por favor, preencha uma data fim!')
        return  
    
    data_inicio = converter_data(data_ini_plantao)
    data_fim = converter_data(data_fim_plantao)
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    c.execute("INSERT INTO plantao_hrs (data_inicio, data_fim) VALUES (?, ?)", (data_inicio, data_fim))
    conn.commit()
    conn.close()
    
    #Exibir mensagem de sucesso na interface
    mensagem_label3.config(text='Dias de plantão inseridos com sucesso!')
    
    #Limpar os campos após salvar as horas extras com sucesso
    cal_inicio.delete(0, "end")
    cal_fim.delete(0, "end")
    
    #Chamar função para limpar mensagem de sucesso ou falha
    config_window.after(5000, lambda: mensagem_label3.config(text=''))
    
# Função para abrir a segunda tela
def abrir_config_horas():
    global cal_dia_hora_extra, entry_quantidade_horas, entry_valor_60, entry_valor_80, entry_valor_100, entry_valor_bip, mensagem_label, cal_quinzena, entry_horas_bip, valor_60, valor_80, valor_100, valor_bip, mensagem_label2, config_window, cal_inicio, cal_fim, mensagem_label3
    
    #Ocultar janela atual
    app.withdraw()
    
    # Criar uma nova janela
    config_window = tk.Toplevel(app)
    config_window.title('Configurar Horas')
    config_window.geometry('1200x700')
    
    #Criação do Label para adicionar horas extras
    label_titulo1 = LabelFrame(config_window, text='Adicionar Horas Extras', font=('Arial', 16, 'bold'))
    label_titulo1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    label_dia = tk.Label(label_titulo1, text='Dia da hora:')
    label_dia.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    
    cal_dia_hora_extra = DateEntry(label_titulo1, date_pattern='dd/mm/yyyy', locale='pt_BR')
    cal_dia_hora_extra.delete(0, tk.END)
    cal_dia_hora_extra.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky='e')
    
    label_quantidade_horas = tk.Label(label_titulo1, text='Quantidade de Horas:')
    label_quantidade_horas.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    
    entry_quantidade_horas = tk.Entry(label_titulo1, width=5)
    entry_quantidade_horas.grid(row=2, column=1, padx=5, pady=10, sticky='e')
    
    botao_salvar = tk.Button(label_titulo1, text='Salvar', command=inserir_horas_extra)
    botao_salvar.grid(row=3, column=0, padx=0, pady=10, sticky='e') 
    
    # Label para exibir a mensagem de sucesso
    mensagem_label = tk.Label(config_window, text='')
    mensagem_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    
    #Criação do Label para adicionar horas BIP
    label_titulo2 = LabelFrame(config_window, text='Adicionar Horas BIP', font=('Arial', 16, 'bold'), labelanchor='n')
    label_titulo2.grid(row=0, column=5, columnspan=6, padx=0, pady=0)
    
    label_data = tk.Label(label_titulo2, text='Semana das horas:')
    label_data.grid(row=1, column=5, padx=10, pady=10, sticky='w')
    
    cal_quinzena = DateEntry(label_titulo2, date_pattern='dd/mm/yyyy', locale='pt_BR')
    cal_quinzena.delete(0, tk.END)
    cal_quinzena.grid(row=1, column=6, padx=0, pady=10, sticky='w')
    
    label_horas_bip = tk.Label(label_titulo2, text='Quantidade de horas:')
    label_horas_bip.grid(row=2, column=5, columnspan=2, padx=10, pady=10, sticky='w')
    
    entry_horas_bip = tk.Entry(label_titulo2, width=5)
    entry_horas_bip.grid(row=2, column=6, padx=40, pady=10, sticky='w')    
    
    botao_salvar_hrbip = tk.Button(label_titulo2, text='Salvar', command=inserir_horas_bip)
    botao_salvar_hrbip.grid(row=3, column=5, columnspan=2, padx=0, pady=10) 
    
    # Label para exibir a mensagem de sucesso
    mensagem_label2 = tk.Label(config_window, text='')
    mensagem_label2.grid(row=4, column=5, columnspan=2, padx=20, pady=10)
    
    #Criação do label para adicionar dias de plantão
    label_titulo4 = LabelFrame(config_window, text='Adicionar Dias de plantão', font=('Arial', 16, 'bold'), labelanchor='n')
    label_titulo4.grid(row=0, column=11, columnspan=5, padx=110, pady=0)
    
    label_data_ini = tk.Label(label_titulo4, text='Data inicio:') 
    label_data_ini.grid(row=1, column=11, padx=10, pady=10)
    
    cal_inicio = DateEntry(label_titulo4, date_pattern='dd/mm/yyyy', locale='pt_BR')
    cal_inicio.delete(0, tk.END)
    cal_inicio.grid(row=1, column=12, padx=10, pady=10)
    
    label_data_fim = tk.Label(label_titulo4, text='Data fim:') 
    label_data_fim.grid(row=2, column=11, padx=10, pady=10)
    
    cal_fim = DateEntry(label_titulo4, date_pattern='dd/mm/yyyy', locale='pt_BR')
    cal_fim.delete(0, tk.END)
    cal_fim.grid(row=2, column=12, padx=10, pady=10)
    
    botao_salvar_dtplantao = tk.Button(label_titulo4, text='Salvar', command=inserir_datas_plantao)
    botao_salvar_dtplantao.grid(row=3, column=12, padx=0, pady=10)
    
    # Label para exibir a mensagem de sucesso
    mensagem_label3 = tk.Label(config_window, text='')
    mensagem_label3.grid(row=4, column=13, padx=0, pady=10)
    
    #Função para limpar a mensagem de sucesso após 5 segundos
    def limpar_mensagem():
        mensagem_label.config(text='')
        mensagem_label2.config(text='')
        mensagem_label3.config(text='')
        
    config_window.after(5000, limpar_mensagem)
    
    def toggle_edit_mode():
        global edit_mode

        # Inverter o valor da variável de controle
        edit_mode = not edit_mode

        # Habilitar/desabilitar a edição dos campos
        entry_valor_60.config(state='normal' if edit_mode else 'disabled')
        entry_valor_80.config(state='normal' if edit_mode else 'disabled')
        entry_valor_100.config(state='normal' if edit_mode else 'disabled')
        entry_valor_bip.config(state='normal' if edit_mode else 'disabled')
    
    label_titulo3 = LabelFrame(config_window, text='Configurar valor de horas extras', font=('Arial', 16, 'bold'))
    label_titulo3.grid(row=7, column=0, columnspan=5, padx=10, pady=10)
    
    label_valor_60 = tk.Label(label_titulo3, text='Valor Hora Extra 60%(Segunda a sexta):')
    label_valor_60.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky='w')
    
    entry_valor_60 = tk.Entry(label_titulo3, width=5, state='normal')
    entry_valor_60.grid(row=8, column=0, columnspan=2, padx=135, pady=10, sticky='e')
    entry_valor_60.insert(0, float(valor_60))
        
    label_valor_80 = tk.Label(label_titulo3, text='Valor Hora Extra 80%(Sabado):')
    label_valor_80.grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky='w')
    
    entry_valor_80 = tk.Entry(label_titulo3, width=5, state='normal')
    entry_valor_80.grid(row=9, column=1, padx=10, pady=10)
    entry_valor_80.insert(0, float(valor_80))
    
    label_valor_100 = tk.Label(label_titulo3, text='Valor Hora Extra 100%(Domingo e feriado):')
    label_valor_100.grid(row=10, column=0, columnspan=4, padx=10, pady=10,  sticky='w')
    
    entry_valor_100 = tk.Entry(label_titulo3, width=5, state='normal')
    entry_valor_100.grid(row=10, column=1, padx=50, pady=10)
    entry_valor_100.insert(0, float(valor_100))
    
    label_valor_bip = tk.Label(label_titulo3, text='Valor Hora BIP:')
    label_valor_bip.grid(row=11, column=0, columnspan=4, padx=10, pady=10,  sticky='w')
    
    entry_valor_bip = tk.Entry(label_titulo3, width=5, state='normal')
    entry_valor_bip.grid(row=11, column=0, columnspan=4, padx=100, pady=10, sticky='w')
    entry_valor_bip.insert(0, float(valor_bip))
  
    # Criar o botão para editar os campos
    botao_editar = tk.Button(label_titulo3, text='Editar', command=toggle_edit_mode)
    botao_editar.grid(row=12, column=0, columnspan=2, padx=10, pady=10)    
    
    # Desabilitar os campos
    entry_valor_60.config(state='disabled')
    entry_valor_80.config(state='disabled')
    entry_valor_100.config(state='disabled')
    entry_valor_bip.config(state='disabled')
       
    # Função para voltar à janela principal
    def voltar_janela_principal():
        #global valor_60, valor_80, valor_100, valor_bip
        
        # Armazenar os valores dos campos
        valor_60 = entry_valor_60.get()
        valor_80 = entry_valor_80.get()
        valor_100 = entry_valor_100.get()
        valor_bip = entry_valor_bip.get()
        
        config_window.destroy()
        app.deiconify()  # Mostrar a janela principal novamente
        atualizar_qtd_horas_extras()
        mostrar_calendario()
    
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
atualizar_qtd_horas_extras()
mostrar_calendario()
app.mainloop()
