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
import shutil
import telebot
import requests

with open ('C:/Users/pdv/Desktop/gabriel/chaveapitelebot.txt', 'r') as chaves:
    for chave in chaves:
        chaveapi = chave

        
bot = telebot.TeleBot(chaveapi)
cnpjs,ljs = [],[]
mensagemID,forn = '',''
mes_global = '01'
lista_lojas = ['LJ1 - Guanabara','LJ2 - Primavera','LJ3 - Iguatemi','LJ4 - Flamboyant',
                   'LJ5 - São Paulo','LJ6 - Valinhos','LJ7 - Ouro Verde', 'ESCOLHIDO']


def makeKeyboard(lista):
    markup = InlineKeyboardMarkup()
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
    global forn,mensagemID,ljs
    ljs=[]
    mensagemID = mensagem.chat.id
    forn = mensagem.text[7:]        
    lojas()
    
    
@bot.message_handler(commands=["oba"])
def notas(mensagem):
    url = 'https://obahortifruti.com.br/ofertas/minha-hora-oba/index.php?regiao=sp-interior'
    response = requests.get(url, stream=True)
    with open('C:/Users/pdv/Desktop/selenium-imgs/interior.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    mensagemID = mensagem.chat.id
    pic = 'C:/Users/pdv/Desktop/selenium-imgs/interior.png'
    bot.send_photo(mensagemID, photo=open(pic,'rb'))

    
@bot.message_handler(commands=["fartura"])
def notas(mensagem):
    url = 'https://www.hortifrutifartura.com.br/wp-content/themes/fartura/images/banner-oferta.png'
    response = requests.get(url, stream=True)
    with open('C:/Users/pdv/Desktop/selenium-imgs/nosso.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    mensagemID = mensagem.chat.id
    pic = 'C:/Users/pdv/Desktop/selenium-imgs/nosso.png'
    bot.send_photo(mensagemID, photo=open(pic,'rb'))


@bot.message_handler(commands=["obasp"])
def notas(mensagem):
    url = 'https://obahortifruti.com.br/ofertas/minha-hora-oba/index.php?regiao=sp'
    response = requests.get(url, stream=True)
    with open('C:/Users/pdv/Desktop/selenium-imgs/sp.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    mensagemID = mensagem.chat.id
    pic = 'C:/Users/pdv/Desktop/selenium-imgs/sp.png'
    bot.send_photo(mensagemID, photo=open(pic,'rb'))
    
    
@bot.message_handler(commands=["dalbem"])
def notas(mensagem):
    mensagemID = mensagem.chat.id
    inita()
    enviadalbem(mensagemID)
    
    
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
    text = '''
    Olá! Seja bem vindo ao NF Fartura Bot
    :D  Estes são os meus Comandos:

    "/notas fornecedor" pra ver notas do fornecedor
    =-=-=-=-=-=-=-=-=-=  OU  =-=-=-=-=-=-=-=-=-=
    "/notas cnpj" (xx.xxx.xxx/xxxx-xx)
    =-=-=-=-=-=-=-=-=-=  OU  =-=-=-=-=-=-=-=-=-=
    "/numero 123456" (número da sua nota)
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    "/dalbem     (p/ ofertas do dalbem)  "
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    "/dalbem     (p/ ofertas do dalbem)  "
    '''
    bot.reply_to(mensagem, text)
    
    
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global lista_lojas,ljs,forn
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
    pasta = r'C:\Users\pdv\Desktop\selenium-imgs\rename'
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




