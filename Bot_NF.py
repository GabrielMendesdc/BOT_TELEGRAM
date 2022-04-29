#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))


# In[ ]:


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from ipynb.fs.full.chamar import init
from ipynb.fs.full.dalbem import inita
import os
import string
import time
from datetime import date
import shutil
import telebot
import requests
from pdf2image import convert_from_path


with open ('C:/Users/pdv/Desktop/gabriel/chaveapitelebot.txt', 'r') as chaves:
    for chave in chaves:
        chaveapi = chave

        
bot = telebot.TeleBot(chaveapi)
cnpjs,ljs = [],[]
mensagemID,forn = '',''
mes_global = '02'
lista_lojas = ['LJ1 - Guanabara','LJ2 - Primavera','LJ3 - Iguatemi','LJ4 - Flamboyant',
                   'LJ5 - São Paulo','LJ6 - Valinhos','LJ7 - Ouro Verde', 'ESCOLHIDO']


def poezero(lista,pos):
    mes = ''
    if lista[pos] <= 9:
        mes = f'0{str(lista[pos])}'
    else:
        mes = f'{str(lista[pos])}'
    return mes


def makeKeyboard(lista):
    markup = InlineKeyboardMarkup()
    if lista[0] == 'meses' or lista[0] == 'will' or lista[0] == 'alex' or lista[0] == 'tdsalex':
        mes1 = poezero(lista,1)
        x1 = lista[0][0]
        xs1 = str(x1) + str(mes1)
        btn = InlineKeyboardButton(mes1, callback_data=xs1)
        mes2 = poezero(lista,2)
        x2 = lista[0][0]
        xs2 = str(x2) + str(mes2)
        btn2 = InlineKeyboardButton(mes2, callback_data=xs2)
        markup.row(btn,btn2)
        print('retornou')
        return markup
    if len(lista) == 8:
        for i in range(len(lista)):
            markup.add(InlineKeyboardButton(str(lista[i]), callback_data=str(lista[i])))
    else:
        for i in range(len(lista)):
            markup.add(InlineKeyboardButton(str(lista[i]), callback_data=str(i)))
    return markup


def lojas():
    global lista_lojas,mensagemID
    bot.send_message(mensagemID,"Escolha quais lojas: ", reply_markup = makeKeyboard(lista_lojas))
    

def mes(codigo='meses'):
    global mensagemID
    lista_meses = [codigo,date.today().month-1,date.today().month]
    print('código: ',codigo)
    bot.send_message(mensagemID,"Escolha quais meses: ", reply_markup = makeKeyboard(lista_meses))
    
    
def checkforn(forn = 'adep',ljs='0123456'):
    global cnpjs,mensagemID, mes_global
    perg,achei,aux,cnpj,cnpjs,k = False,False,[],'',[],0
    with open("cnpjs.txt", 'r') as db:
        for linha in db:
            if forn in linha.lower():
                cnpj = linha[-19:-9]
                cnpj = ''.join([i for i in cnpj if i not in string.punctuation])
                cnpjs.append(int(cnpj))
                aux.append(linha)
                k+=1
                if achei:
                    perg = True
                achei = True
    if not achei:
        bot.send_message(mensagemID, 'não achei esse fornecedor')
        return 0
    if perg:
        if len(aux) == 8:
            aux.append('fornecedor fantasma pra nao atrapalhar o sistema')
        bot.send_message(mensagemID,"Escolha seu fornecedor: ", reply_markup = makeKeyboard(aux))
        return 1
    if achei and perg == False:
        try:
            global mes_global
            init(int(cnpj),loja=ljs,idz=mensagemID,mes=mes_global)
            envia(mensagemID)
        except Exception as e:
            print(e)
            bot.send_message(mensagemID, 'não encontrei notas. desculpe, error :',e)


@bot.message_handler(commands=["notas"])
def notas(mensagem):
    global forn,ljs,mensagemID
    ljs=[]
    mensagemID = mensagem.chat.id
    forn = mensagem.text[7:]  
    mes()
    lojas()
    

@bot.message_handler(commands=["oba"])
def oba(mensagem):
#     url = 'https://obahortifruti.com.br/ofertas/minha-hora-oba/index.php?regiao=sp'
    pasta = 'C:/Users/pdv/Desktop/selenium-imgs/oba'
    mensagemID = mensagem.chat.id
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            pic = f'{pasta}\\{arquivo}'
            bot.send_photo(mensagemID, photo=open(pic,'rb'))
            
            
@bot.message_handler(commands=["goodbom"])
def goodbom(mensagem):
#     url = 'https://goodbom.com.br/tabloides/index.php/goodbom-taquaral/'
    pasta = 'C:/Users/pdv/Desktop/selenium-imgs/goodbom'
    mensagemID = mensagem.chat.id
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            pic = f'{pasta}\\{arquivo}'
            bot.send_photo(mensagemID, photo=open(pic,'rb'))
            
    
@bot.message_handler(commands=["fartura"])
def fartura(mensagem):
    mensagemID = mensagem.chat.id
    pasta = 'C:/Users/pdv/Desktop/selenium-imgs/nosso'
    mensagemID = mensagem.chat.id
    for diretorio, subpastas, arquivos in os.walk(pasta):
        if arquivos:
            for arquivo in arquivos:
                pic = f'{pasta}\\{arquivo}'
                bot.send_photo(mensagemID, photo=open(pic,'rb'))
        else:
            texto = 'sem panfleto hj'
            bot.send_message(mensagemID,texto)


@bot.message_handler(commands=["obasp"])
def obasp(mensagem):
#     url = 'https://obahortifruti.com.br/ofertas/minha-hora-oba/index.php?regiao=sp'
    mensagemID = mensagem.chat.id
    pic = 'C:/Users/pdv/Desktop/selenium-imgs/sp.png'
    bot.send_photo(mensagemID, photo=open(pic,'rb'))
    
    
@bot.message_handler(commands=["dalbem"])
def dalbem(mensagem):
    mensagemID = mensagem.chat.id
    enviadalbem(mensagemID)
    

@bot.message_handler(commands=["pgmenos"])
def pgmenos(mensagem):
    #https://www.superpaguemenos.com.br/tabloide-digital/s
    pasta = 'C:/Users/pdv/Desktop/selenium-imgs/pgmenos/feito'
    mensagemID = mensagem.chat.id
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            pic = f'{pasta}\\{arquivo}'
            bot.send_photo(mensagemID, photo=open(pic,'rb'))
           

@bot.message_handler(commands=["alextds"])
def alextds(mensagem):
    global mensagemID
    mensagemID = mensagem.chat.id
    mes('tdsalex')
        
        
@bot.message_handler(commands=["alex"])
def alex(mensagem):
    global mensagemID
    mensagemID = mensagem.chat.id
    mes('alex')

        
@bot.message_handler(commands=["will"])
def will(mensagem):
    global mensagemID
    mensagemID = mensagem.chat.id
    mes('will')


@bot.message_handler(commands=["numero"])
def numero(mensagem):
    msg = str(int(mensagem.text[8:]))
    global forn,mensagemID,ljs, mes_global
    ljs=[]
    mensagemID = mensagem.chat.id
    if len(msg) >= 3 and msg.isdigit() == True:
        print(f'por cnpj: {msg}')
        init(numero=msg,idz=mensagemID,mes=mes_global)
        envia(mensagemID)
    else:
        bot.send_message(mensagemID,"Não use letras ou menos de 3 números")

    
@bot.message_handler(func=lambda message: True)
def resposta(mensagem):
    text = '''Olá! Seja bem vindo ao NF Fartura Bot
    
    ^^  Estes são os meus Comandos:

    PARA PUXAR NOTAS FISCAIS:
    /notas <nome do fornecedor>
    /notas <cnpjdofornecedor>
    
    PARA PUXAR NOTAS PELO NUMERO DE NOTA:
    /numero <n°NF> (ex: /numero 15945)
    
    PARA PUXAR OFERTAS DO DALBEM: /dalbem
    
    PARA PUXAR OFERTAS DO OBA: /oba
    
    PARA PUXAR OFERTAS PAGUE MENOS: /pgmenos
    
    PARA PUXAR OFERTAS GOODBOM: /goodbom

    PARA PUXAR OFERTAS FARTURA: /fartura
    
    PARA PUXAR TODAS AS OFERTAS: /ofertas
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='''
    bot.reply_to(mensagem, text)
    
    
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global lista_lojas,ljs,forn,mes_global
    if call.data.startswith('t') == True:
        dados01 = ['=-=-=-=-=-=-=açougue:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.13 % de crescimento', '2° dezena:  0.13 % de crescimento', '3° dezena:  0.04 % de crescimento', 'Total:  0.1 % de crescimento', 'loja 2:', '1° dezena:  0.09 % de crescimento', '2° dezena:  0.03 % de crescimento', '3° dezena:  0.14 % de crescimento', 'Total:  0.09 % de crescimento', 'loja 3:', '1° dezena:  -0.06 % de crescimento', '2° dezena:  -0.0 % de crescimento', '3° dezena:  0.1 % de crescimento', 'Total:  0.02 % de crescimento', 'loja 4:', '1° dezena:  -0.07 % de crescimento', '2° dezena:  -0.01 % de crescimento', '3° dezena:  -0.07 % de crescimento', 'Total:  -0.05 % de crescimento', 'loja 5:', '1° dezena:  0.03 % de crescimento', '2° dezena:  0.04 % de crescimento', '3° dezena:  0.06 % de crescimento', 'Total:  0.05 % de crescimento', 'loja 6:', '1° dezena:  0.09 % de crescimento', '2° dezena:  0.08 % de crescimento', '3° dezena:  0.04 % de crescimento', 'Total:  0.07 % de crescimento', 'loja 7:', '1° dezena:  -0.11 % de crescimento', '2° dezena:  -0.19 % de crescimento', '3° dezena:  -0.25 % de crescimento', 'Total:  -0.19 % de crescimento', '=-=-=-=-=-=-=frios:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.21 % de crescimento', '2° dezena:  -0.08 % de crescimento', '3° dezena:  -0.16 % de crescimento', 'Total:  -0.15 % de crescimento', 'loja 2:', '1° dezena:  -0.11 % de crescimento', '2° dezena:  -0.06 % de crescimento', '3° dezena:  -0.12 % de crescimento', 'Total:  -0.1 % de crescimento', 'loja 3:', '1° dezena:  -0.21 % de crescimento', '2° dezena:  0.0 % de crescimento', '3° dezena:  -0.21 % de crescimento', 'Total:  -0.15 % de crescimento', 'loja 4:', '1° dezena:  -0.19 % de crescimento', '2° dezena:  -0.11 % de crescimento', '3° dezena:  -0.26 % de crescimento', 'Total:  -0.2 % de crescimento', 'loja 5:', '1° dezena:  -0.14 % de crescimento', '2° dezena:  -0.13 % de crescimento', '3° dezena:  -0.28 % de crescimento', 'Total:  -0.2 % de crescimento', 'loja 6:', '1° dezena:  -0.09 % de crescimento', '2° dezena:  -0.14 % de crescimento', '3° dezena:  -0.4 % de crescimento', 'Total:  -0.25 % de crescimento', 'loja 7:', '1° dezena:  -0.07 % de crescimento', '2° dezena:  0.05 % de crescimento', '3° dezena:  -0.21 % de crescimento', 'Total:  -0.09 % de crescimento', '=-=-=-=-=-=-=auto serviço:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.18 % de crescimento', '2° dezena:  -0.02 % de crescimento', '3° dezena:  0.01 % de crescimento', 'Total:  -0.06 % de crescimento', 'loja 2:', '1° dezena:  -0.05 % de crescimento', '2° dezena:  0.1 % de crescimento', '3° dezena:  0.19 % de crescimento', 'Total:  0.09 % de crescimento', 'loja 3:', '1° dezena:  -0.16 % de crescimento', '2° dezena:  0.06 % de crescimento', '3° dezena:  0.04 % de crescimento', 'Total:  -0.02 % de crescimento', 'loja 4:', '1° dezena:  -0.14 % de crescimento', '2° dezena:  -0.03 % de crescimento', '3° dezena:  -0.04 % de crescimento', 'Total:  -0.07 % de crescimento', 'loja 5:', '1° dezena:  -0.03 % de crescimento', '2° dezena:  0.03 % de crescimento', '3° dezena:  0.14 % de crescimento', 'Total:  0.05 % de crescimento', 'loja 6:', '1° dezena:  -0.01 % de crescimento', '2° dezena:  0.03 % de crescimento', '3° dezena:  -0.1 % de crescimento', 'Total:  -0.04 % de crescimento', 'loja 7:', '1° dezena:  -0.1 % de crescimento', '2° dezena:  0.13 % de crescimento', '3° dezena:  0.08 % de crescimento', 'Total:  0.04 % de crescimento', '=-=-=-=-=-=-=mercearia:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.25 % de crescimento', '2° dezena:  -0.12 % de crescimento', '3° dezena:  -0.17 % de crescimento', 'Total:  -0.18 % de crescimento', 'loja 2:', '1° dezena:  -0.12 % de crescimento', '2° dezena:  -0.02 % de crescimento', '3° dezena:  -0.06 % de crescimento', 'Total:  -0.07 % de crescimento', 'loja 3:', '1° dezena:  -0.21 % de crescimento', '2° dezena:  -0.04 % de crescimento', '3° dezena:  -0.1 % de crescimento', 'Total:  -0.12 % de crescimento', 'loja 4:', '1° dezena:  -0.23 % de crescimento', '2° dezena:  -0.13 % de crescimento', '3° dezena:  -0.24 % de crescimento', 'Total:  -0.21 % de crescimento', 'loja 5:', '1° dezena:  -0.11 % de crescimento', '2° dezena:  -0.14 % de crescimento', '3° dezena:  -0.16 % de crescimento', 'Total:  -0.14 % de crescimento', 'loja 6:', '1° dezena:  -0.14 % de crescimento', '2° dezena:  -0.13 % de crescimento', '3° dezena:  -0.29 % de crescimento', 'Total:  -0.2 % de crescimento', 'loja 7:', '1° dezena:  -0.06 % de crescimento', '2° dezena:  -0.08 % de crescimento', '3° dezena:  -0.29 % de crescimento', 'Total:  -0.17 % de crescimento']
        dados02 = ['=-=-=-=-=-=-=açougue:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.18 % de crescimento', '2° dezena:  0.0 % de crescimento', 'loja 2:', '1° dezena:  0.15 % de crescimento', '2° dezena:  0.08 % de crescimento', 'loja 3:', '1° dezena:  0.21 % de crescimento', '2° dezena:  0.14 % de crescimento', 'loja 4:', '1° dezena:  0.2 % de crescimento', '2° dezena:  0.11 % de crescimento', 'loja 5:', '1° dezena:  0.14 % de crescimento', '2° dezena:  0.05 % de crescimento', 'loja 6:', '1° dezena:  0.22 % de crescimento', '2° dezena:  0.17 % de crescimento', 'loja 7:', '1° dezena:  0.05 % de crescimento', '2° dezena:  0.13 % de crescimento', '=-=-=-=-=-=-=frios:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.27 % de crescimento', '2° dezena:  0.11 % de crescimento', 'loja 2:', '1° dezena:  0.19 % de crescimento', '2° dezena:  0.15 % de crescimento', 'loja 3:', '1° dezena:  0.26 % de crescimento', '2° dezena:  0.17 % de crescimento', 'loja 4:', '1° dezena:  0.26 % de crescimento', '2° dezena:  0.24 % de crescimento', 'loja 5:', '1° dezena:  0.19 % de crescimento', '2° dezena:  0.12 % de crescimento', 'loja 6:', '1° dezena:  0.1 % de crescimento', '2° dezena:  0.19 % de crescimento', 'loja 7:', '1° dezena:  0.01 % de crescimento', '2° dezena:  0.05 % de crescimento', '=-=-=-=-=-=-=auto serviço:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.18 % de crescimento', '2° dezena:  0.16 % de crescimento', 'loja 2:', '1° dezena:  0.18 % de crescimento', '2° dezena:  0.15 % de crescimento', 'loja 3:', '1° dezena:  0.23 % de crescimento', '2° dezena:  0.13 % de crescimento', 'loja 4:', '1° dezena:  0.2 % de crescimento', '2° dezena:  0.28 % de crescimento', 'loja 5:', '1° dezena:  0.27 % de crescimento', '2° dezena:  0.23 % de crescimento', 'loja 6:', '1° dezena:  0.13 % de crescimento', '2° dezena:  0.16 % de crescimento', 'loja 7:', '1° dezena:  0.02 % de crescimento', '2° dezena:  -0.04 % de crescimento', '=-=-=-=-=-=-=mercearia:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.27 % de crescimento', '2° dezena:  0.13 % de crescimento', 'loja 2:', '1° dezena:  0.19 % de crescimento', '2° dezena:  0.15 % de crescimento', 'loja 3:', '1° dezena:  0.26 % de crescimento', '2° dezena:  0.15 % de crescimento', 'loja 4:', '1° dezena:  0.2 % de crescimento', '2° dezena:  0.19 % de crescimento', 'loja 5:', '1° dezena:  0.17 % de crescimento', '2° dezena:  0.21 % de crescimento', 'loja 6:', '1° dezena:  0.14 % de crescimento', '2° dezena:  0.2 % de crescimento', 'loja 7:', '1° dezena:  0.02 % de crescimento', '2° dezena:  0.05 % de crescimento']
        if call.data[1:] == '01':
            for i in dados01:
                bot.send_message(mensagemID,i)
        if call.data[1:] == '02':
            for i in dados02:
                bot.send_message(mensagemID,i)
        return
    
    if call.data.startswith('a') == True:
        dados01 = ['=-=-=-=-=-=-=açougue:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  0.09 % de crescimento', '2° dezena:  0.03 % de crescimento', '3° dezena:  0.14 % de crescimento', 'Total:  0.09 % de crescimento', '=-=-=-=-=-=-=frios:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  -0.11 % de crescimento', '2° dezena:  -0.06 % de crescimento', '3° dezena:  -0.12 % de crescimento', 'Total:  -0.1 % de crescimento', '=-=-=-=-=-=-=auto serviço:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  -0.05 % de crescimento', '2° dezena:  0.1 % de crescimento', '3° dezena:  0.19 % de crescimento', 'Total:  0.09 % de crescimento', '=-=-=-=-=-=-=mercearia:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  -0.12 % de crescimento', '2° dezena:  -0.02 % de crescimento', '3° dezena:  -0.06 % de crescimento', 'Total:  -0.07 % de crescimento']
        dados02 = ['=-=-=-=-=-=-=açougue:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  0.15 % de crescimento', '2° dezena:  0.08 % de crescimento', '=-=-=-=-=-=-=frios:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  0.19 % de crescimento', '2° dezena:  0.15 % de crescimento', '=-=-=-=-=-=-=auto serviço:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  0.18 % de crescimento', '2° dezena:  0.15 % de crescimento', '=-=-=-=-=-=-=mercearia:=-=-=-=-=-=-=', 'loja 2:', '1° dezena:  0.19 % de crescimento', '2° dezena:  0.15 % de crescimento']
        if call.data[1:] == '01':
            for i in dados01:
                bot.send_message(mensagemID,i)
        if call.data[1:] == '02':
            for i in dados02:
                bot.send_message(mensagemID,i)
        return
    
    if call.data.startswith('w') == True:
        dados01 = ['=-=-=-=-=-=-=açougue:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.06 % de crescimento', '2° dezena:  -0.05 % de crescimento', '3° dezena:  -0.11 % de crescimento', 'Total:  -0.08 % de crescimento', 'loja 2:', '1° dezena:  0.04 % de crescimento', '2° dezena:  0.08 % de crescimento', '3° dezena:  0.12 % de crescimento', 'Total:  0.08 % de crescimento', 'loja 3:', '1° dezena:  -0.04 % de crescimento', '2° dezena:  -0.18 % de crescimento', '3° dezena:  -0.11 % de crescimento', 'Total:  -0.11 % de crescimento', 'loja 4:', '1° dezena:  -0.13 % de crescimento', '2° dezena:  -0.1 % de crescimento', '3° dezena:  -0.12 % de crescimento', 'Total:  -0.12 % de crescimento', 'loja 5:', '1° dezena:  0.08 % de crescimento', '2° dezena:  0.05 % de crescimento', '3° dezena:  0.05 % de crescimento', 'Total:  0.06 % de crescimento', 'loja 6:', '1° dezena:  -0.06 % de crescimento', '2° dezena:  -0.16 % de crescimento', '3° dezena:  -0.11 % de crescimento', 'Total:  -0.11 % de crescimento', 'loja 7:', '1° dezena:  -0.11 % de crescimento', '2° dezena:  0.01 % de crescimento', '3° dezena:  -0.13 % de crescimento', 'Total:  -0.08 % de crescimento', '=-=-=-=-=-=-=frios:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.02 % de crescimento', '2° dezena:  -0.0 % de crescimento', '3° dezena:  0.0 % de crescimento', 'Total:  -0.15 % de crescimento', 'loja 2:', '1° dezena:  0.07 % de crescimento', '2° dezena:  0.08 % de crescimento', '3° dezena:  0.08 % de crescimento', 'Total:  -0.1 % de crescimento', 'loja 3:', '1° dezena:  -0.1 % de crescimento', '2° dezena:  -0.07 % de crescimento', '3° dezena:  -0.08 % de crescimento', 'Total:  -0.15 % de crescimento', 'loja 4:', '1° dezena:  -0.04 % de crescimento', '2° dezena:  -0.11 % de crescimento', '3° dezena:  -0.08 % de crescimento', 'Total:  -0.2 % de crescimento', 'loja 5:', '1° dezena:  0.03 % de crescimento', '2° dezena:  0.09 % de crescimento', '3° dezena:  0.08 % de crescimento', 'Total:  -0.2 % de crescimento', 'loja 6:', '1° dezena:  -0.12 % de crescimento', '2° dezena:  -0.19 % de crescimento', '3° dezena:  -0.17 % de crescimento', 'Total:  -0.25 % de crescimento', 'loja 7:', '1° dezena:  -0.04 % de crescimento', '2° dezena:  0.02 % de crescimento', '3° dezena:  -0.06 % de crescimento', 'Total:  -0.09 % de crescimento', '=-=-=-=-=-=-=auto serviço:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.25 % de crescimento', '2° dezena:  -0.25 % de crescimento', '3° dezena:  -0.24 % de crescimento', 'Total:  -0.06 % de crescimento', 'loja 2:', '1° dezena:  0.01 % de crescimento', '2° dezena:  0.11 % de crescimento', '3° dezena:  0.1 % de crescimento', 'Total:  0.09 % de crescimento', 'loja 3:', '1° dezena:  -0.07 % de crescimento', '2° dezena:  -0.11 % de crescimento', '3° dezena:  -0.07 % de crescimento', 'Total:  -0.02 % de crescimento', 'loja 4:', '1° dezena:  -0.13 % de crescimento', '2° dezena:  -0.16 % de crescimento', '3° dezena:  -0.12 % de crescimento', 'Total:  -0.07 % de crescimento', 'loja 5:', '1° dezena:  -0.01 % de crescimento', '2° dezena:  0.0 % de crescimento', '3° dezena:  -0.03 % de crescimento', 'Total:  0.05 % de crescimento', 'loja 6:', '1° dezena:  -0.2 % de crescimento', '2° dezena:  -0.23 % de crescimento', '3° dezena:  -0.2 % de crescimento', 'Total:  -0.04 % de crescimento', 'loja 7:', '1° dezena:  -0.09 % de crescimento', '2° dezena:  0.08 % de crescimento', '3° dezena:  -0.07 % de crescimento', 'Total:  0.04 % de crescimento', '=-=-=-=-=-=-=mercearia:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.15 % de crescimento', '2° dezena:  -0.1 % de crescimento', '3° dezena:  -0.08 % de crescimento', 'Total:  -0.18 % de crescimento', 'loja 2:', '1° dezena:  0.02 % de crescimento', '2° dezena:  0.08 % de crescimento', '3° dezena:  0.07 % de crescimento', 'Total:  -0.07 % de crescimento', 'loja 3:', '1° dezena:  -0.11 % de crescimento', '2° dezena:  -0.08 % de crescimento', '3° dezena:  -0.1 % de crescimento', 'Total:  -0.12 % de crescimento', 'loja 4:', '1° dezena:  -0.12 % de crescimento', '2° dezena:  -0.1 % de crescimento', '3° dezena:  -0.11 % de crescimento', 'Total:  -0.21 % de crescimento', 'loja 5:', '1° dezena:  -0.05 % de crescimento', '2° dezena:  -0.02 % de crescimento', '3° dezena:  -0.04 % de crescimento', 'Total:  -0.14 % de crescimento', 'loja 6:', '1° dezena:  -0.18 % de crescimento', '2° dezena:  -0.15 % de crescimento', '3° dezena:  -0.2 % de crescimento', 'Total:  -0.2 % de crescimento', 'loja 7:', '1° dezena:  0.05 % de crescimento', '2° dezena:  0.18 % de crescimento', '3° dezena:  0.01 % de crescimento', 'Total:  -0.17 % de crescimento']
        dados02 = ['=-=-=-=-=-=-=açougue:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.08 % de crescimento', '2° dezena:  -0.03 % de crescimento', 'loja 2:', '1° dezena:  0.2 % de crescimento', '2° dezena:  0.1 % de crescimento', 'loja 3:', '1° dezena:  -0.06 % de crescimento', '2° dezena:  -0.08 % de crescimento', 'loja 4:', '1° dezena:  0.0 % de crescimento', '2° dezena:  -0.14 % de crescimento', 'loja 5:', '1° dezena:  0.07 % de crescimento', '2° dezena:  0.11 % de crescimento', 'loja 6:', '1° dezena:  0.1 % de crescimento', '2° dezena:  -0.07 % de crescimento', 'loja 7:', '1° dezena:  0.03 % de crescimento', '2° dezena:  0.01 % de crescimento', '=-=-=-=-=-=-=frios:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  0.01 % de crescimento', '2° dezena:  0.06 % de crescimento', 'loja 2:', '1° dezena:  0.16 % de crescimento', '2° dezena:  0.15 % de crescimento', 'loja 3:', '1° dezena:  -0.05 % de crescimento', '2° dezena:  0.04 % de crescimento', 'loja 4:', '1° dezena:  0.0 % de crescimento', '2° dezena:  0.08 % de crescimento', 'loja 5:', '1° dezena:  0.1 % de crescimento', '2° dezena:  0.09 % de crescimento', 'loja 6:', '1° dezena:  -0.12 % de crescimento', '2° dezena:  -0.1 % de crescimento', 'loja 7:', '1° dezena:  0.06 % de crescimento', '2° dezena:  0.01 % de crescimento', '=-=-=-=-=-=-=auto serviço:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.24 % de crescimento', '2° dezena:  -0.01 % de crescimento', 'loja 2:', '1° dezena:  0.1 % de crescimento', '2° dezena:  0.31 % de crescimento', 'loja 3:', '1° dezena:  -0.15 % de crescimento', '2° dezena:  0.02 % de crescimento', 'loja 4:', '1° dezena:  -0.15 % de crescimento', '2° dezena:  0.04 % de crescimento', 'loja 5:', '1° dezena:  0.07 % de crescimento', '2° dezena:  0.13 % de crescimento', 'loja 6:', '1° dezena:  -0.2 % de crescimento', '2° dezena:  -0.14 % de crescimento', 'loja 7:', '1° dezena:  -0.16 % de crescimento', '2° dezena:  -0.11 % de crescimento', '=-=-=-=-=-=-=mercearia:=-=-=-=-=-=-=', 'loja 1:', '1° dezena:  -0.02 % de crescimento', '2° dezena:  0.01 % de crescimento', 'loja 2:', '1° dezena:  0.12 % de crescimento', '2° dezena:  0.19 % de crescimento', 'loja 3:', '1° dezena:  -0.08 % de crescimento', '2° dezena:  -0.06 % de crescimento', 'loja 4:', '1° dezena:  -0.06 % de crescimento', '2° dezena:  0.03 % de crescimento', 'loja 5:', '1° dezena:  0.01 % de crescimento', '2° dezena:  0.1 % de crescimento', 'loja 6:', '1° dezena:  -0.16 % de crescimento', '2° dezena:  -0.1 % de crescimento', 'loja 7:', '1° dezena:  0.08 % de crescimento', '2° dezena:  0.07 % de crescimento']
        if call.data[1:] == '01':
            for i in dados01:
                bot.send_message(mensagemID,i)
        if call.data[1:] == '02':
            for i in dados02:
                bot.send_message(mensagemID,i)
        return
    
    if call.data.startswith('m') == True:
        mes_global = call.data[1:]
        return
    
    if call.data.isdigit():
        try:
            iniciar(call.data)
        except Exception as e:
            bot.send_message(mensagemID, 'não encontrei notas. desculpe, erro ',e)
    else:
        if call.data == 'ESCOLHIDO' and ljs:
            checkforn(forn,ljs)
        if str(lista_lojas.index(call.data)) not in ljs and call.data != 'ESCOLHIDO':
            ljs.append(str(lista_lojas.index(call.data)))
        
        
def envia(mensagemID):
    k=0
    pasta = fr'C:\Users\pdv\projetos_jupyter\retorno\\{mensagemID}'
    for diretorio, subpastas, arquivos in os.walk(pasta):
        if not arquivos:
            text = 'Desculpe, não achei notas desse fornecedor nessa loja'
            bot.send_message(mensagemID,text)
            return 0
        for arquivo in arquivos:
            j=str(k)+'.'
            x = f'{pasta}\\nota{j}png'
            k+= 1
            bot.send_photo(mensagemID, photo=open(x,'rb'))
    text = 'pronto :)'
    bot.send_message(mensagemID,text)
    
    
def enviadalbem(mensagemID):
    pasta = r'C:\Users\pdv\Desktop\selenium-imgs\dalbem\feito'
    for diretorio, subpastas, arquivos in os.walk(pasta):
        if not arquivos:
            text = 'Desculpe, não achei as ofertas do dalbem'
            bot.send_message(mensagemID,text)
            return 0
        for arquivo in arquivos:
            x = f'{pasta}\\{arquivo}'
            bot.send_photo(mensagemID, photo=open(x,'rb'))
    text = 'pronto :)'
    bot.send_message(mensagemID,text)
    
    
def iniciar(calldata):
    global cnpjs,mensagemID,ljs, mes_global
    try:
        r = init(cnpjs[int(calldata)],loja=ljs,idz=mensagemID,mes=mes_global)
        envia(mensagemID)
    except Exception as e:
        print(e)
        bot.reply_to(mensagemID, 'não achei notas')
    if r == "não achei esse":
        bot.reply_to(mensagemID, r)

        
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)


# In[ ]:





# In[ ]:




