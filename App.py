import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from datetime import date, datetime, timedelta
import calendar
import locale
import sqlite3
from tkcalendar import DateEntry
import requests
import confs
import matplotlib.pyplot as plt
import pickle
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mplcursors 
import pysqlcipher3
from pysqlcipher3 import dbapi2 as sqlite

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Variáveis globais para os campos de entrada
hoje = date.today()
dia = hoje.day
mes = hoje.month
ano = hoje.year

mes_anterior = mes - 1

#Adicionar zeros a esquerda do hoje e do mes quando necessairo
mes_formatado = str(mes).zfill(2)
mes_anterior_formatado = str(mes_anterior).zfill(2)

#Parametros para API
pais = 'BR'
chave_api = confs.api_key
url = f'https://calendarific.com/api/v2/holidays?country={pais}&year={ano}&api_key={chave_api}'

entry_dia = None
entry_hora = None
entry_quantidade_horas = None
entry_valor_60 = None
entry_valor_80 = None
entry_valor_100 = None
entry_valor_bip = None

total_horas_semana = 0
total_horas_sabado = 0
total_horas_domingo = 0
total_horas_bip = 0
valor_total = 0
dsr_total = 0

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    
    # Verificar se a resposta contém os feriados
    if 'response' in dados and 'holidays' in dados['response']:
        feriados = dados['response']['holidays']
    else:
        print('Nenhum feriado encontrado.')
else:
    print('Erro na solicitação.')

#Função para abrir tela de inicio
def abrir_inicio():
    global menu_principal, menubar, app, qtd_horas_extras_segsex, qtd_horas_extras_sab, qtd_horas_extras_domfer, qtd_horas_bips, vlr_horas_extras_segsex, vlr_horas_extras_sab, vlr_horas_extras_domfer, vlr_horas_bips, vlr_total, calendar_frame, header_label, vlr_dsr
    
    #Tela
    app = tk.Tk()
    app.title('Controle de Horas Extras')
    app.resizable(False, False)
    app.geometry('1200x700')
                    
    #Criar os widgets
    header_label = tk.Label(app, text='', font=('Arial', 30, 'bold'))
    header_label.grid(row=0, column=0, columnspan=2, padx=140, pady=10, sticky='w')

    calendar_frame = tk.Frame(app)
    calendar_frame.grid(row=1, column=0, columnspan=7, padx=10, pady=10, rowspan=8, sticky='w')   

    label_titulo = tk.Label(app, text=f'Valores calculados do dia 16/0{mes_anterior} até o dia 15/0{mes}', font=('Arial', 18, 'bold'))
    label_titulo.grid(row=0, column=3, columnspan=2, sticky='w', padx=50)

    #Campos de informações de qtd de horas e valores
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

    label51 = tk.Label(app, text='Total DSR:', font=('Arial', 15, 'bold'))
    label51.grid(row=9, column=3, padx=70, sticky='w')
    
    vlr_dsr = tk.Label(app, font=('Arial', 15))
    vlr_dsr.grid(row=9, column=3, columnspan=2, padx=180, sticky='w')
    
    label61 = tk.Label(app, text='Total a receber:', font=('Arial', 15, 'bold'))
    label61.grid(row=10, column=3, padx=70, sticky='w')

    vlr_total = tk.Label(app, font=('Arial', 15))
    vlr_total.grid(row=10, column=3, columnspan=2, padx=230, sticky='w')

    #Legendas para o calendario
    bck_lgd_cal = tk.Label(app, bg='purple')
    bck_lgd_cal.grid(row=9, column=0, padx=20, sticky='w')

    label_lgd_cal = tk.Label(app, text='Dias de plantão', font=('Arial', 15, 'bold'))
    label_lgd_cal.grid(row=9, column=0, padx=50, sticky='w')

    bck_lgd_cal = tk.Label(app, bg='red')
    bck_lgd_cal.grid(row=10, column=0, padx=20, sticky='w')

    label_lgd_fer = tk.Label(app, text='Feriados no mês', font=('Arial', 15, 'bold'))
    label_lgd_fer.grid(row=10, column=0, padx=50, sticky='w')

    #Criar a menu bar
    menubar = Menu(app)
    app.config(menu=menubar)
    
    #Criar os itens do menu    
    menubar.add_command(label='CONFIGURAR HORAS ', command=abrir_config_horas)
    menubar.add_command(label='RESULTADOS ', command=abrir_resultado)
    menubar.add_command(label='SAIR', command=app.quit)

    #Criar o menu
    menu_principal = tk.Menu(menubar, tearoff=0)

#Função para criar o calendario
def mostrar_calendario(feriados):
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
        
    #Obter o primeiro dia do mês atual
    primeiro_dia_mes = datetime(ano, mes, 1)

    #Obter o dia da semana do primeiro dia do mês (0 = domingo, 6 = sabado)
    primeiro_dia_semana = primeiro_dia_mes.weekday()

    #Obter o ultimo dia do mês anterior
    ultimo_dia_mes_anterior = primeiro_dia_mes - timedelta(days=1)
    ultimo_dia_mes_anterior = ultimo_dia_mes_anterior.day
    mes_anterior = mes - 1
    
    #Calcular o número de dias no mês atual
    num_dias_mes_atual = calendar.monthrange(ano, mes)[1]
    
    # Obter o último dia do mês atual
    ultimo_dia_mes_atual = calendar.monthrange(ano, mes)[1]

    # Obter o primeiro dia do próximo mês
    primeiro_dia_proximo_mes = primeiro_dia_mes + timedelta(days=ultimo_dia_mes_atual)
    
    #Preencher a primeira semana do mês com os dias do mês anterior
    primeira_semana_mes = cal[0] 
    for day in range(len(primeira_semana_mes) -1, -1, -1):
        if primeira_semana_mes[day] == 0:
            cal[0][day] = ultimo_dia_mes_anterior
            ultimo_dia_mes_anterior -= 1

    #Preencher a ultima semana do mês com os dias do proximo mês
    ult_semana_mes = cal[-1]
    prox_mes_dia = 1
    for day in range(len(ult_semana_mes)):
        if ult_semana_mes[day] == 0:
            cal[-1][day] = prox_mes_dia
            prox_mes_dia += 1
            
    #Resgatar os resultados da consulta no banco de dados com as datas que estarei de plantão
    datas_plantao = []
    for data_inicio, data_fim in resultado5:
        dia_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        dia_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        datas_plantao.append((dia_inicio, dia_fim))

    #Preencher os dias do calendário
    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            #Dias do mês atual
            data_obj = datetime(ano, mes, day).date()
            data_api = datetime(ano, mes, day).date()
                
            #Preencher dias de plantão
            for dia_inicio, dia_fim in datas_plantao:
                if dia_inicio <= data_obj <= dia_fim:
                    label = tk.Label(calendar_frame, text=str(day).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised', bg='purple')
                    break
                    
                #Preencher, se houver, os feriados no mês
                for feriado in feriados:
                    if data_api == feriado['date']:
                        label = tk.Label(calendar_frame, text=str(day).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised', fg='red')
                        break
                    else:
                        label = tk.Label(calendar_frame, text=str(day).zfill(2), padx=10, pady=5, font=('Arial', 35), relief='raised')
            label.grid(row=week_num+1, column=day_num, sticky='e')           

        
#Função para contar dias uteis, feriados e domingos do mes atual
def contar_dias_uteis(ano, mes, feriados):
    total_dias_uteis = 0
    total_feriados = 0
    total_domingos = 0
    num_dias_mes_atual = calendar.monthrange(ano, mes)[1]
    
    for day in range(1, num_dias_mes_atual + 1):
        data_obj = datetime(ano, mes, day).date()
        dia_semana = data_obj.weekday()

        #Verifica se o dia não é feriado
        if data_obj in feriados:
            total_feriados += 1
        
        #Verifica se o dia é um domingo (dia_semana = 6)
        elif dia_semana == 6:
            total_domingos += 1
                        
        else:
            total_dias_uteis += 1
            
    return total_dias_uteis, total_feriados, total_domingos    

#Função para atualizar as quantidades de horas e os valores
def atualizar_qtd_horas_extras():
    global total_horas_semana, total_horas_sabado, total_horas_domingo, total_horas_bip, hoje, mes, ano, mes_anterior, resultado5, valor_total, dsr_total
    global qtd_horas_extras_segsex, qtd_horas_extras_sab, qtd_horas_extras_domfer, qtd_horas_bips, vlr_horas_extras_segsex, vlr_horas_extras_sab, vlr_horas_extras_domfer, vlr_horas_bips, vlr_total
    
    #limpar as variaveis de horas
    total_horas_semana = 0
    total_horas_sabado = 0
    total_horas_domingo = 0
    total_horas_bip = 0
    valor_total = 0
    dsr_total = 0
    
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
    
    carregar_valores_horas()
    
    vlr_hora_60 = str(hora_60).replace(',', '.').replace('R$', '').replace(' ', '')
    vlr_hora_80 = str(hora_80).replace(',', '.').replace('R$', '').replace(' ', '')
    vlr_hora_100 = str(hora_100).replace(',', '.').replace('R$', '').replace(' ', '')
    vlr_hora_bip = str(hora_bip).replace(',', '.').replace('R$', '').replace(' ', '')
    
    if vlr_hora_60 is not None:
        resultado_segsex = total_horas_semana * float(vlr_hora_60)
        resultado_segsex_decimal = '{:.2f}'.format(resultado_segsex) #Deixar somente com 2 casas decimais e arredontar 
        resultado_segsex_str = str(resultado_segsex_decimal).replace('.', ',')
        vlr_horas_extras_segsex.config(text=f"R$ {resultado_segsex_str}")
    else:
        None
    
    if vlr_hora_80 is not None:
        resultado_sab = total_horas_sabado * float(vlr_hora_80)
        resultado_sab_decimal = '{:.2f}'.format(resultado_sab) #Deixar somente com 2 casas decimais e arredontar 
        resultado_sab_str = str(resultado_sab_decimal).replace('.', ',')
        vlr_horas_extras_sab.config(text=f"R$ {resultado_sab_str}")
    else:
        None
        
    if vlr_hora_100 is not None:
        resultado_dom = total_horas_domingo * float(vlr_hora_100)
        resultado_dom_format = '{:.2f}'.format(resultado_dom) #Deixar somente com 2 casas decimais e arredontar
        resultado_dom_str = str(resultado_dom_format).replace('.', ',')
        vlr_horas_extras_domfer.config(text=f"R$ {resultado_dom_str}")
    else:
        None
        
    if vlr_hora_bip is not None:
        resultado_bip = total_horas_bip * float(vlr_hora_bip)
        resultado_bip_decimal = '{:.2f}'.format(resultado_bip) #Deixar somente com 2 casas decimais e arredontar 
        resultado_bip_str = str(resultado_bip_decimal).replace('.', ',')
        vlr_horas_bips.config(text=f"R$ {resultado_bip_str}")
    else:
        None
    
    dias_uteis_mes, feriados_mes, domingos_mes = contar_dias_uteis(ano, mes, feriados)
    feriados_domingos = feriados_mes + domingos_mes 
        
    #Calcular DSR sobre as horas BIP
    dsr_bip = (resultado_bip / dias_uteis_mes) * feriados_domingos
    dsr_bip_decimal = '{:.2f}'.format(dsr_bip) #Deixar somente com 2 casas decimais e arredontar
    dsr_bip_str = str(dsr_bip_decimal).replace('.', ',')
    
    #Calcular DSR sobre horas extras 60%
    dsr_hr_60 = ((total_horas_semana / dias_uteis_mes) * feriados_domingos) * float(vlr_hora_60)
    dsr_hr_60_decimal = '{:.2f}'.format(dsr_hr_60) #Deixar somente com 2 casas decimais e arredontar
    dsr_hr_60_str = str(dsr_hr_60_decimal).replace('.', ',')

    #Calcular DSR sobre horas extras 80%
    dsr_hr_80 = ((total_horas_sabado / dias_uteis_mes) * feriados_domingos) * float(vlr_hora_80)
    dsr_hr_80_decimal = '{:.2f}'.format(dsr_hr_80) #Deixar somente com 2 casas decimais e arredontar
    dsr_hr_80_str = str(dsr_hr_80_decimal).replace('.', ',')
    
    #Calcular DSR sobre horas extras 100%
    dsr_hr_100 = ((total_horas_domingo / dias_uteis_mes) * feriados_domingos) * float(vlr_hora_100)
    dsr_hr_100_decimal = '{:.2f}'.format(dsr_hr_100) #Deixar somente com 2 casas decimais e arredontar
    dsr_hr_100_str = str(dsr_hr_100_decimal).replace('.', ',')
     
    #Mostrar valor de DSR sobre os valores na tela
    dsr_total = dsr_bip + dsr_hr_60 + dsr_hr_80 + dsr_hr_100
    dsr_total_decimal = '{:.2f}'.format(dsr_total) #Deixar somente com 2 casas decimais e arredontar
    dsr_total_str = str(dsr_total_decimal).replace('.', ',')
    vlr_dsr.config(text=f'R$ {dsr_total_str}')
        
    #Calcular total a receber de acordo com valores ja mostrados na tela
    valor_total = (resultado_bip + resultado_dom + resultado_sab + resultado_segsex) + dsr_total
    valor_total_decimal = '{:.2f}'.format(valor_total) #Deixar somente com 2 casas decimais e arredontar
    valor_total_str = str(valor_total_decimal).replace('.', ',')
    vlr_total.config(text=f'R$ {valor_total_str}')
    
    #Chamar função de atualizar valor total no banco de dados
    inserir_total_mes()

def criar_abrir_db():
    conn = pysqlcipher3.connect('horas.db')
    cria_db_key(conn, confs.db_key)
    return conn

def cria_db_key(conn, chave):
    conn.execute(f"PRAGM key = '{chave}';")
        

#Função para criar a tabela no banco de dados
def criar_tabela(conn):
    #conn = sqlite3.connect('horas.db')
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
    c.execute('''CREATE TABLE IF NOT EXISTS ganho_mes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mes_data DATE,
                    total_mes FLOAT,
                    dsr_mes FLOAT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS salario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vlr_salario FLOAT,
                    qtd_horas_trab INT)''')
    conn.commit()
    conn.close()
    
#Função para converter a data no formato "dd/mm/aaaa" para o formato adequado do SQLite("aaaa-mm-dd")
def converter_data(data):
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    data_sqlite = data_obj.strftime("%Y-%m-%d")
    return data_sqlite

#Função para inserir horas extras no banco de dados
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

#Função para inserir datas de plantão no banco de dados
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
    
#Função para inserir ou atualizar o total ganho no mês atual no banco de dados
def inserir_total_mes():
    #Pegar a ultima data do mês atual
    ultimo_dia = calendar.monthrange(ano, mes)[1]       

    #Concatenar a data para salvar no banco de dados
    data = str(ultimo_dia) + '/' + str(mes) + '/' + str(ano)
    
    #Converter a data para padrão do sqlite
    data_mes = converter_data(data)
    
    valor_salario = '{:.2f}'.format(valor_total)    
    valor_dsr = '{:.2f}'.format(dsr_total)
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    
    #Verificar se o registro ja existe
    consulta = ("SELECT * FROM ganho_mes WHERE mes_data = ?")
    c.execute(consulta, (data_mes,))
    registro = c.fetchone()
    
    #Se não existir insere
    if registro is None:
        insercao = ("INSERT INTO ganho_mes (mes_data, total_mes, dsr_mes) VALUES (?, ?, ?)")
        c.execute(insercao, (data_mes, valor_salario, valor_dsr))
    #Se existir atualiza se for diferente
    elif registro[2] != valor_salario:
        atualizar = ("UPDATE ganho_mes SET total_mes = ?, dsr_mes = ? WHERE mes_data = ?")
        c.execute(atualizar, (valor_salario, valor_dsr, data_mes))
    
    conn.commit()
    conn.close()
        
#Função para salvar os valores do salario e sempre que entrar na tela estar com ele
def salvar_valores():
    #Obter os valores dos campos de entrada
    salario = entry_salario.get()
    horas_trabalhadas = entry_horas.get()

    #Serializar e salvar os valores em um arquivo
    with open("valores_salarios.pickle", "wb") as file:
        pickle.dump({"salario": salario, "horas_trabalhadas": horas_trabalhadas}, file)
        
#Função para carregar os valores salvar no arquivo
def carregar_valores():
    try:
        #Carregar os valores do arquivo, se existir
        with open("valores_salarios.pickle", "rb") as file:
            valores = pickle.load(file)
            salario = valores["salario"]
            horas_trabalhadas = valores["horas_trabalhadas"]

            #Exibir os valores nos campos de entrada
            entry_salario.config(state='normal')
            entry_salario.delete(0, tk.END)
            entry_salario.insert(0, salario)
            entry_salario.config(state='disabled')

            entry_horas.config(state='normal')
            entry_horas.delete(0, tk.END)
            entry_horas.insert(0, horas_trabalhadas)
            entry_horas.config(state='disabled')

    except FileNotFoundError:
        #Se o arquivo não existir (primeira execução), não faz nada
        pass

#Função para salvar os valores das horas
def salvar_valores_horas():
    vlr_hora_60 = entry_valor_60.get()
    vlr_hora_80 = entry_valor_80.get()
    vlr_hora_100 = entry_valor_100.get()
    vlr_hora_bip = entry_valor_bip.get() 

    #Serializar e salvar os valores em um arquivo
    with open('valores_horas.pickle', 'wb') as file:
        pickle.dump({'vlr_hora_60': vlr_hora_60, 'vlr_hora_80': vlr_hora_80, 'vlr_hora_100': vlr_hora_100, 'vlr_hora_bip': vlr_hora_bip}, file)
    
#Função para carregar os valores das horas
def carregar_valores_horas():
    global hora_60, hora_80, hora_100, hora_bip
    
    try:
        #Carregar os valores do arquivo, se existir
        with open("valores_horas.pickle", "rb") as file:
            valores = pickle.load(file)
            hora_60 = valores["vlr_hora_60"]
            hora_80 = valores["vlr_hora_80"]
            hora_100 = valores["vlr_hora_100"]
            hora_bip = valores["vlr_hora_bip"]

    except FileNotFoundError:
        #Se o arquivo não existir (primeira execução), não faz nada
        pass    

#Função para calcular valores das horas extras de acordo com o salario
def calcular_valores_horas():
    #global valor_hora_trab_f, valor_hora_60_f, valor_hora_80_f, valor_hora_100_f, valor_hora_bip_f
    
    sal = entry_salario.get()
    if sal.strip() != '':
        salario = float(entry_salario.get().replace(',', '.').replace('R$', '').replace(' ', ''))
        horas = int(entry_horas.get())
        
        valor_hora_trab = salario / horas
        valor_hora_trab_f = float('{:.2f}'.format(valor_hora_trab))
            
        valor_hora_60 = (valor_hora_trab_f * 0.6) + valor_hora_trab_f
        valor_hora_60_f = f'R$ {valor_hora_60:.2f}'
        entry_valor_60.config(state='normal')
        entry_valor_60.insert(0, valor_hora_60_f.replace('.', ','))
        entry_valor_60.config(state='disabled')
                    
        valor_hora_80 = (valor_hora_trab_f * 0.8) + valor_hora_trab_f
        valor_hora_80_f = f'R$ {valor_hora_80:.2f}'
        entry_valor_80.config(state='normal')
        entry_valor_80.insert(0, valor_hora_80_f.replace('.', ','))
        entry_valor_80.config(state='disabled')
        
        valor_hora_100 = (valor_hora_trab_f * 1) + valor_hora_trab_f
        valor_hora_100_f = f'R$ {valor_hora_100:.2f}'
        entry_valor_100.config(state='normal')
        entry_valor_100.insert(0, valor_hora_100_f.replace('.', ','))
        entry_valor_100.config(state='disabled')            
            
        valor_hora_bip = valor_hora_trab_f / 2.859
        valor_hora_bip_f = f'R$ {valor_hora_bip:.2f}'
        entry_valor_bip.config(state='normal')
        entry_valor_bip.insert(0, valor_hora_bip_f.replace('.', ','))
        entry_valor_bip.config(state='disabled')
        
#Função para abrir a tela de configurar horas
def abrir_config_horas():
    global cal_dia_hora_extra, entry_quantidade_horas, entry_valor_60, entry_valor_80, entry_valor_100, entry_valor_bip, mensagem_label, cal_quinzena, entry_horas_bip, valor_60, valor_80, valor_100, valor_bip, mensagem_label2, config_window, cal_inicio, cal_fim, mensagem_label3
    global entry_salario, entry_horas
    
    #Ocultar janela atual
    app.withdraw()
    
    #Criar uma nova janela
    config_window = tk.Toplevel(app)
    config_window.title('Configurar Horas')
    config_window.resizable(False, False)
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
    
    #Label para exibir a mensagem de sucesso
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
    
    #Label para exibir a mensagem de sucesso
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
    
    #Label para exibir a mensagem de sucesso
    mensagem_label3 = tk.Label(config_window, text='')
    mensagem_label3.grid(row=4, column=13, padx=0, pady=10)
    
    #Função para limpar a mensagem de sucesso após 5 segundos
    def limpar_mensagem():
        mensagem_label.config(text='')
        mensagem_label2.config(text='')
        mensagem_label3.config(text='')
        
    config_window.after(5000, limpar_mensagem)
        
    #Função para cadastrar novo salario no banco de dados
    def pop_cadastro():
        # Criar a janela de diálogo
        popup_cadastro = tk.Toplevel(config_window)
        popup_cadastro.title('Cadastro de Salário e Horas')
        popup_cadastro.resizable(False, False)

        # Label e entry para o salário
        label_salario_cad = tk.Label(popup_cadastro, text='Salário mensal:')
        label_salario_cad.grid(row=0, column=0, padx=10, pady=5)

        entry_salario_cad = tk.Entry(popup_cadastro, width=10)
        entry_salario_cad.grid(row=0, column=1, padx=10, pady=5)

        # Label para horas fixas
        label_horas_cad = tk.Label(popup_cadastro, text='Horas trabalhadas no mês:')
        label_horas_cad.grid(row=1, column=0, padx=10, pady=5)

        entry_horas_fixas = tk.Label(popup_cadastro, text='220', state='disabled')
        entry_horas_fixas.grid(row=1, column=1, padx=10, pady=5)
    
        def salvar_cadastro():
            salario = entry_salario_cad.get()
            
            #Verifica se o valor digitado é numérico
            if salario.replace('.', '', 1).isdigit():
                salario_float = float(salario)
                conn = sqlite3.connect('horas.db')
                c = conn.cursor()
                
                #Verifica se já existe registro na tabela "salario"
                c.execute("SELECT * FROM salario")
                if c.fetchone() is not None:
                    #Caso exista, atualiza o valor do salário
                    c.execute("UPDATE salario SET vlr_salario = ?, qtd_horas_trab = 220", (salario_float,))
                else:
                    #Caso não exista, insere o valor do salário
                    c.execute("INSERT INTO salario (vlr_salario, qtd_horas_trab) VALUES (?, 220)", (salario_float,))
                conn.commit()
                conn.close()
                popup_cadastro.destroy()
            else:
                # Mostra mensagem de erro caso o valor digitado não seja numérico
                tk.messagebox.showerror('Erro', 'Por favor, digite um valor numérico para o salário, com o padrão 0000.00.')

        # Botão para salvar os dados digitados
        botao_salvar_cad = tk.Button(popup_cadastro, text='Salvar', command=salvar_cadastro)
        botao_salvar_cad.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    #Função para selecionar o salario
    def popup_selecionar_salarios():
        
        #Criar a janela de diálogo
        popup_salarios = tk.Toplevel(config_window)
        popup_salarios.title('Selecionar Salário')
        popup_salarios.resizable(False, False)

        #Criar o widget Listbox para mostrar os salários
        lista_salarios = tk.Listbox(popup_salarios, selectmode=tk.SINGLE, exportselection=False)
        lista_salarios.grid(row=0, column=0, padx=10, pady=10)
        
        #Função para preencher o Listbox com os salários cadastrados
        def preencher_lista_salarios():
            conn = sqlite3.connect('horas.db')
            c = conn.cursor()

            #Obter os valores cadastrados na tabela "salario"
            c.execute("SELECT vlr_salario FROM salario")
            valores_cadastrados = c.fetchall()

            conn.close()

            #Adicionar os valores cadastrados ao Listbox
            for valor in valores_cadastrados:
                lista_salarios.insert(tk.END, valor[0])

        #Chamar a função para preencher a lista de salários ao abrir a janela
        preencher_lista_salarios()
    
        #Função para selecionar o salário e atualizar o entry_salario
        def selecionar_salario():
            #Obter o valor selecionado pelo usuário no Listbox
            salario_selecionado = lista_salarios.get(lista_salarios.curselection())
            
            salario_formatado = f'R$ {salario_selecionado:.2f}'

            #Atualizar o campo de entrada (entry_salario) com o valor selecionado
            entry_salario.config(state='normal')
            entry_salario.delete(0, tk.END)
            entry_salario.insert(0, str(salario_formatado).replace('.', ','))
            entry_salario.config(state='disabled')
            
            #Atualizar o campo de entrada (entry_horas) com o valor de 220
            entry_horas.config(state='normal')
            entry_horas.delete(0, tk.END)
            entry_horas.insert(0, '220')
            entry_horas.config(state='disabled')
            
            #Fechar a janela de diálogo
            popup_salarios.destroy()
            
            salvar_valores()
            carregar_valores()
            
            calcular_valores_horas()
            #app.after(1000, calcular_valores_horas)

        #Botão para selecionar o salário e chamar a função selecionar_salario
        botao_selecionar_salario = tk.Button(popup_salarios, text='Selecionar', command=selecionar_salario)
        botao_selecionar_salario.grid(row=1, column=0, padx=10, pady=10)
    
    #Frame de configurar valores
    label_titulo3 = LabelFrame(config_window, text='Configurar Valores', font=('Arial', 16, 'bold'), labelanchor='n')
    label_titulo3.grid(row=7, column=0, columnspan=5, padx=5, pady=10)
    
    label_salario = tk.Label(label_titulo3, text='Salário mensal:')
    label_salario.grid(row=8, column=0, padx=5, pady=5, sticky='w')
    
    entry_salario = tk.Entry(label_titulo3, width=10, state='disabled')
    entry_salario.grid(row=8, column=0, padx=0, pady=5, sticky='e')
    
    label_horas = tk.Label(label_titulo3, text='Horas trabalhadas no mês:')
    label_horas.grid(row=9, column=0, padx=5, pady=5, sticky='w')
    
    entry_horas = tk.Entry(label_titulo3, width=4, state='disabled')
    entry_horas.grid(row=9, column=1, padx=0, pady=5, sticky='w')
    
    #Carregar, se houver, valores no arquivo
    carregar_valores()
    
    label_valor_60 = tk.Label(label_titulo3, text='Valor hora extra 60%(seg à sex):')
    label_valor_60.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky='w')
    
    entry_valor_60 = tk.Entry(label_titulo3, width=8, state='disabled')
    entry_valor_60.grid(row=10, column=1, padx=25, pady=5, sticky='e')
        
    label_valor_80 = tk.Label(label_titulo3, text='Valor hora extra 80%(sab):')
    label_valor_80.grid(row=11, column=0, padx=5, pady=5, sticky='w')
    
    entry_valor_80 = tk.Entry(label_titulo3, width=8, state='disabled')
    entry_valor_80.grid(row=11, column=1, padx=0, pady=5, sticky='w')

    label_valor_100 = tk.Label(label_titulo3, text='Valor hora extra 100%(dom):')
    label_valor_100.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    
    entry_valor_100 = tk.Entry(label_titulo3, width=8, state='disabled')
    entry_valor_100.grid(row=12, column=1, padx=10, pady=5, sticky='w')
   
    label_valor_bip = tk.Label(label_titulo3, text='Valor hora BIP:')
    label_valor_bip.grid(row=13, column=0, padx=5, pady=5, sticky='w')
    
    entry_valor_bip = tk.Entry(label_titulo3, width=8, state='disabled')
    entry_valor_bip.grid(row=13, column=0, padx=10, pady=5, sticky='e')
    vlr_60 = entry_valor_bip.get()
    
    calcular_valores_horas()
    
    #Botão para selecionar e cadastrar salario
    botao_selecionar = tk.Button(label_titulo3, text='Selecionar', command=popup_selecionar_salarios)
    botao_selecionar.grid(row=14, column=0, padx=5, pady=10, sticky='w')
    
    botao_cadastro = tk.Button(label_titulo3, text='Cadastrar', command=pop_cadastro)
    botao_cadastro.grid(row=14, column=0, padx=0, pady=10, sticky='e')
    
    vlr_sal = entry_salario.get()
    if not vlr_sal.strip() == '':
        if vlr_60.strip() == '':
            salvar_valores_horas()
        
    #Verificar qual botão foi clicado para abrir a nova tela
    def verificar_click_btn_menu(botao):        
        if botao == 'INICIO':
            abrir_inicio()
            atualizar_qtd_horas_extras()
            mostrar_calendario(feriados)
            config_window.destroy()
        if botao == 'RESULTADO':
            abrir_resultado()
            atualizar_qtd_horas_extras()
            mostrar_calendario(feriados)
            config_window.destroy()
            
    #Criar o menu na janela de configuração de horas
    menubar_config = tk.Menu(config_window)
    config_window.config(menu=menubar_config)
    
    #Criar o item de menu "INICIO"
    menubar_config.add_command(label='INICIO ', command=lambda: verificar_click_btn_menu('INICIO'))
    menubar_config.add_command(label='RESULTADOS ', command=lambda: verificar_click_btn_menu('RESULTADOS'))
    menubar_config.add_command(label='SAIR ', command=app.quit)
    
    #Configurar o evento para fechar a janela
    config_window.protocol("WM_DELETE_WINDOW", encerrar_programa)
      
#Função para filtrar os valores a apartir da data selecionada
def filtrar_valores():
    data = cal_filtro.get()
        
    if data is None or data == '':
        data_atual = datetime.today()
        data_filtro = data_atual - timedelta(days=365)
    else:
        data_filtro = converter_data(data)
    
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    
    consulta = ("SELECT total_mes + dsr_mes AS total_ganho_mes, mes_data FROM ganho_mes WHERE mes_data >= ? ORDER BY mes_data ASC LIMIT 12")
    c.execute(consulta, (data_filtro,))
    
    resultados = c.fetchall()
    
    labels_vlr_mes = [vlr_mes1, vlr_mes2, vlr_mes3, vlr_mes4, vlr_mes5,
                      vlr_mes6, vlr_mes7, vlr_mes8, vlr_mes9, vlr_mes10,
                      vlr_mes11, vlr_mes12]
    
    labels_nome_mes = [label_mes1, label_mes2, label_mes3, label_mes4, 
                       label_mes5, label_mes6, label_mes7, label_mes8, 
                       label_mes9, label_mes10, label_mes11, label_mes12]
    
    data_x = []
    valores_y = []
    
    #Atualiza o valor do Label com o valor obtido do banco de dados
    for i, resultado in enumerate(resultados):
        if i < len(labels_vlr_mes):
            if resultado[0] is not None:
                valor_formatado = '{:.2f}'.format(resultado[0])
                labels_vlr_mes_str = str(valor_formatado).replace('.', ',')
                labels_vlr_mes[i].config(text=f'R$ {labels_vlr_mes_str}')
                
                #Extrair mês e ano das datas e preencher no frame
                mes_data = datetime.strptime(resultado[1], '%Y-%m-%d') #convertar string para date
                nome_mes = mes_data.strftime('%B').capitalize()
                ano = mes_data.year
                labels_nome_mes[i].config(text=f'{nome_mes} de {ano}')
                data_x.append(mes_data.strftime('%b %Y'))  # Adiciona o mês e ano formatado à lista
                valores_y.append(resultado[0])  # Adiciona o valor recebido à lista        
    
    #Caso tenham menos de 12 registros, limpa os demais Labels
    for i in range(len(resultados), 12):
        labels_vlr_mes[i].config(text='')
        labels_nome_mes[i].config(text='')
    
    conn.close()      
    
    #Cria o gráfico de linhas somente se houver valores preenchidos
    if valores_y:
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        line, = ax.plot(data_x, valores_y, marker='o', color='b', linestyle='-', label='Valores')
        ax.set_xlabel('Mês e Ano', fontweight='bold')
        ax.set_ylabel('Quantidade de Valores Recebidos', fontweight='bold')
        ax.set_title('Valores Recebidos por Mês(em R$)', fontweight='bold', fontsize=16)
        ax.grid(True)
        ax.legend()
        
        #Rotaciona as legendas do eixo X na diagonal
        ax.set_xticklabels(data_x, rotation=45, ha='right')
        
        #Adiciona os valores das linhas diretamente no gráfico
        for x, y in zip(data_x, valores_y):
            ax.text(x, y, f'{y:.2f}', ha='left', va='top', fontweight='bold')
            
        #Move a legenda para o canto inferior esquerdo
        ax.legend(loc='lower right')           
        
        #Cria um objeto FigureCanvasTkAgg para incorporar o gráfico no tkinter
        canvas = FigureCanvasTkAgg(fig, master=resultados_window)
        canvas.draw()
        
        canvas.get_tk_widget().grid(row=9, column=0, columnspan=12, padx=10, pady=10)
       
#Função para abrir a tela de resultados        
def abrir_resultado():    
    global vlr_mes1, vlr_mes2, vlr_mes3, vlr_mes4, vlr_mes5, vlr_mes6, vlr_mes7, vlr_mes8, vlr_mes9, vlr_mes10, vlr_mes11, vlr_mes12, cal_filtro
    global label_mes1, label_mes2, label_mes3, label_mes4, label_mes5, label_mes6, label_mes7, label_mes8, label_mes9, label_mes10, label_mes10, label_mes11, label_mes12
    global resultados_window
    
    #Ocultar janela atual
    app.withdraw()       
    
    #Criar uma nova janela
    resultados_window = tk.Toplevel(app)
    resultados_window.title('Resultados dos meses')
    resultados_window.resizable(False, False)
    resultados_window.geometry('1200x900')
    
    #Criação do Label para adicionar horas extras
    label_titulo4 = tk.Label(resultados_window, text='Valores Recebidos Por Mês', font=('Arial', 25, 'bold'))
    label_titulo4.grid(row=0, column=0, columnspan=12, padx=0, pady=10)
    
    #Label primeiro mês
    label_mes1 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes1.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes1 = tk.Label(label_mes1, text='Total recebido:')
    label_vlr_mes1.grid(row=2, column=0, padx=2, pady=10, sticky='w')
    
    vlr_mes1 = tk.Label(label_mes1, width=9, state='disabled')
    vlr_mes1.grid(row=2, column=1, padx=2, pady=10, sticky='w')
    
    #Label segundo mês
    label_mes2 = LabelFrame(resultados_window,  font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes2.grid(row=1, column=2, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes2 = tk.Label(label_mes2, text='Total recebido:')
    label_vlr_mes2.grid(row=2, column=2, padx=2, pady=10, sticky='w')
    
    vlr_mes2 = tk.Label(label_mes2, width=9, state='disabled')
    vlr_mes2.grid(row=2, column=3, padx=2, pady=10, sticky='w')
    
    #Label terceiro mês
    label_mes3 = LabelFrame(resultados_window,  font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes3.grid(row=1, column=4, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes3 = tk.Label(label_mes3, text='Total recebido:')
    label_vlr_mes3.grid(row=2, column=4, padx=2, pady=10, sticky='w')
    
    vlr_mes3 = tk.Label(label_mes3, width=9, state='disabled')
    vlr_mes3.grid(row=2, column=5, padx=2, pady=10, sticky='w')
    
    #Label quarto mês
    label_mes4 = LabelFrame(resultados_window,  font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes4.grid(row=1, column=6, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes4 = tk.Label(label_mes4, text='Total recebido:')
    label_vlr_mes4.grid(row=2, column=6, padx=2, pady=10, sticky='w')
    
    vlr_mes4 = tk.Label(label_mes4, width=9, state='disabled')
    vlr_mes4.grid(row=2, column=7, padx=2, pady=10, sticky='w')
    
    #Label quinto mês
    label_mes5 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes5.grid(row=1, column=8, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes5 = tk.Label(label_mes5, text='Total recebido:')
    label_vlr_mes5.grid(row=2, column=8, padx=2, pady=10, sticky='w')
    
    vlr_mes5 = tk.Label(label_mes5, width=9, state='disabled')
    vlr_mes5.grid(row=2, column=9, padx=2, pady=10, sticky='w')
    
    #Label sexto mês
    label_mes6 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes6.grid(row=1, column=10, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes6 = tk.Label(label_mes6, text='Total recebido:')
    label_vlr_mes6.grid(row=2, column=10, padx=2, pady=10, sticky='w')
    
    vlr_mes6 = tk.Label(label_mes6, width=9, state='disabled')
    vlr_mes6.grid(row=2, column=11, padx=2, pady=10, sticky='w')
    
    #Label setimo mês
    label_mes7 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes7.grid(row=4, column=0, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes7 = tk.Label(label_mes7, text='Total recebido:')
    label_vlr_mes7.grid(row=5, column=0, padx=2, pady=10, sticky='w')
    
    vlr_mes7 = tk.Label(label_mes7, width=9, state='disabled')
    vlr_mes7.grid(row=5, column=1, padx=2, pady=10, sticky='w')
    
    #Label oitavo mês
    label_mes8 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes8.grid(row=4, column=2, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes8 = tk.Label(label_mes8, text='Total recebido:')
    label_vlr_mes8.grid(row=5, column=2, padx=2, pady=10, sticky='w')
    
    vlr_mes8 = tk.Label(label_mes8, width=9, state='disabled')
    vlr_mes8.grid(row=5, column=3, padx=2, pady=10, sticky='w')
    
    #Label nono mês
    label_mes9 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes9.grid(row=4, column=4, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes9 = tk.Label(label_mes9, text='Total recebido:')
    label_vlr_mes9.grid(row=5, column=4, padx=2, pady=10, sticky='w')
    
    vlr_mes9 = tk.Label(label_mes9, width=9, state='disabled')
    vlr_mes9.grid(row=5, column=5, padx=2, pady=10, sticky='w')
    
    #Label decimo mês
    label_mes10 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes10.grid(row=4, column=6, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes10 = tk.Label(label_mes10, text='Total recebido:')
    label_vlr_mes10.grid(row=5, column=6, padx=2, pady=10, sticky='w')
    
    vlr_mes10 = tk.Label(label_mes10, width=9, state='disabled')
    vlr_mes10.grid(row=5, column=7, padx=2, pady=10, sticky='w')
    
    #Label decimo primero mês
    label_mes11 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes11.grid(row=4, column=8, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes11 = tk.Label(label_mes11, text='Total recebido:')
    label_vlr_mes11.grid(row=5, column=8, padx=2, pady=10, sticky='w')
    
    vlr_mes11 = tk.Label(label_mes11, width=9, state='disabled')
    vlr_mes11.grid(row=5, column=9, padx=2, pady=10, sticky='w')
    
    #Label decimo segundo mês
    label_mes12 = LabelFrame(resultados_window, font=('Arial', 12, 'bold'), labelanchor='n')
    label_mes12.grid(row=4, column=10, columnspan=2, padx=15, pady=10, sticky='w')
    
    label_vlr_mes12 = tk.Label(label_mes12, text='Total recebido:')
    label_vlr_mes12.grid(row=5, column=10, padx=2, pady=10, sticky='w')
    
    vlr_mes12 = tk.Label(label_mes12, width=9, state='disabled')
    vlr_mes12.grid(row=5, column=11, padx=2, pady=10, sticky='w')
    
    #Criação do calendario para selecionar data de filtro
    cal_filtro = DateEntry(resultados_window, date_pattern='dd/mm/yyyy', locale='pt_BR')
    cal_filtro.delete(0, tk.END)
    cal_filtro.grid(row=7, column=5, padx=10, pady=10, sticky='e')
    
    #Botão para filtrar de acordo com a data
    btn_filtrar = tk.Button(resultados_window, text='Filtrar', command=filtrar_valores)
    btn_filtrar.grid(row=7, column=6, padx=0, pady=0, sticky='w')
    
    #Verificar qual botão foi clicado para abrir a nova tela
    def verificar_click_btn_menu(botao):        
        if botao == 'INICIO':
            abrir_inicio()
            atualizar_qtd_horas_extras()
            mostrar_calendario(feriados)
            resultados_window.destroy()
        if botao == 'CONFIGURAR HORAS':
            abrir_config_horas()
            atualizar_qtd_horas_extras()
            mostrar_calendario(feriados)
            resultados_window.destroy()
    
    #Criar o menu na janela de configuração de horas
    menubar_config = tk.Menu(resultados_window, font=('Arial', 20, 'bold'))
    resultados_window.config(menu=menubar_config)
    
    #Criar o item de menu "INICIO"
    menubar_config.add_command(label='INICIO ', command=lambda: verificar_click_btn_menu('INICIO'))
    menubar_config.add_command(label='CONFIGURAR HORAS ', command=lambda: verificar_click_btn_menu('CONFIGURAR HORAS'))
    menubar_config.add_command(label='SAIR ', command=app.quit)
    
    #Configurar o evento para fechar a janela
    resultados_window.protocol("WM_DELETE_WINDOW", encerrar_programa)
    
#Verificar se ha salarios registrados no banco para poder fazer os calculos do programa
def verificar_salario_db():
    conn = sqlite3.connect('horas.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM salario")
    resultado = c.fetchone()
    
    conn.close()
        
    if resultado and resultado[0] > 0:
        None
    else:
        resposta = messagebox.askquestion('Nenhum Salario Cadastrado',
                                          'Não há nenhum salario cadastrado para que sejam feitas os calculos de horas, por gentileza cadastrar.\n'
                                          'Gostaria de cadastrar um novo salario?',
                                          icon='warning')
        if resposta == 'yes':
            abrir_config_horas()
        else:
            encerrar_programa()

#Função para fechar o programa
def encerrar_programa():
    app.quit()
            
abrir_inicio()
criar_tabela()
atualizar_qtd_horas_extras()
mostrar_calendario(feriados)
verificar_salario_db()
app.mainloop()