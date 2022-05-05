from os import listdir, path
import xml.etree.ElementTree as ET
import re


class User:
    def __init__(self, id_):
        self.id_ = id_
        self.notas = []

    def add_notas(self, nota):
        if nota and type(list()) == type(nota):
            for n in nota:
                self.notas.append(Nota(n))
        elif nota and type(str()) == type(nota):
            self.notas.append(Nota(nota))


nome_lojas = {"05349537000185": 'LJ1 - GUANABARA', "07246178000166": 'LJ2 - PRIMAVERA',
              "08158815000105": 'LJ3 - IGUATEMI', '32265622000138': 'LJ4 - FLAMBOYANT',
              "05349537000266": 'LJ5 - SÃO PAULO', '23017342000209': 'LJ6 - VALINHOS',
              "23017342000110": 'LJ7 - OURO VERDE'}


class Nota:
    def __init__(self, caminho):
        self.caminho = caminho
        self.info = {}
        self.produtos = []
        self.loja = caminho[-71:-57]
        for k, v in nome_lojas.items():
            if self.loja == k:
                self.loja = v
        self.parser()

    def __repr__(self):
        return f'Nota de número: {self.caminho[-23:-14]}'

    def parser(self):
        prod = None
        dicionario_nota = {'nNF': '', 'dhEmi': '', 'dhSaiEnt': '', 'xFant': ''}

        dicionario_prod = {'xProd': '', 'CFOP': '', 'vProd': '', 'cEANTrib': '', 'uCom': '', 'uTrib': '',
                           'qTrib': '', 'vDesc': '', 'vICMSST': '', 'vFCPST': '', 'vIPI': '', 'infAdProd': ''}

        zeros = {'0.0', '0.00', '0.000'}
        arvore = ET.parse(self.caminho)
        raiz = arvore.getroot()
        for filho in raiz.iter():
            if filho.tag[36:] in dicionario_nota.keys():
                self.info[filho.tag[36:]] = filho.text
                print(self.info)
            if filho.tag[36:] == 'det':
                digitos = filho.attrib['nItem']
                if prod:
                    self.produtos.append(prod)
                prod = Produto(digitos)
            if filho.tag[36:] == 'total':
                self.produtos.append(prod)
            if filho.tag[36:] in dicionario_prod.keys():
                if filho.text and filho.text not in zeros:
                    prod.info[filho.tag[36:]] = filho.text
                # self.produtos.append()
        print(self.produtos)



class Produto:
    lista_boni = {'5910', '5911', '5912', '5912', '5913', '5914', '5915', '5916', '5917', '5918', '5919', '1201',
                  '1202', '1203', '1204', '1208', '1209', '1212', '1410', '1411', '1503', '1504', '1505', '1506',
                  '1553', '1660', '1661', '1662', '1918', '1919', '2201', '2202', '2203', '2204', '2208', '2209',
                  '2212', '2410', '2411', '2503', '2504', '2505', '2506', '2553', '2660', '2661', '2662', '2918',
                  '2919', '5201', '5202', '5208', '5209', '5210', '5410', '5411', '5412', '5413', '5503', '5553',
                  '5555', '5556', '5660', '5661', '5662', '5918', '5919', '5921', '6201', '6202', '6208', '6209',
                  '6210', '6410', '6411', '6412', '6413', '6503', '6553', '6555', '6556', '6660', '6661', '6662',
                  '6918', '6919', '6921', '7201', '7202', '7210', '7211', '7212', '7553', '7556'}

    def __init__(self, index):
        self.index = index
        self.info = {}



    def __repr__(self):
        return f'ID {self.index} info: {self.info}\n'


def busca_xmls(cnpj, mes, loja, numero):
    lojas = [0, '05349537000185', '07246178000166', '08158815000105', '32265622000138',
             '05349537000266', '23017342000209', '23017342000110']

    ljs = [lojas[int(i)] for i in loja]

    for lj in ljs:
        dire = path.join('N:\\', 'XML ENTRADA', 'destinadas', lj, f'2022-{mes}')
        if cnpj:
            arq = [path.join(dire, f) for f in listdir(dire) if str(cnpj) in f]
        else:
            arq = [path.join(dire, f) for f in listdir(dire) if str(numero) in f]
        return arq


def init(id_, cnpj, mes, loja, numero=0):
    usuario = User(id_)
    notas = busca_xmls(cnpj, mes, loja, numero)
    if not notas:
        return None
    print(notas)
    usuario.add_notas(notas)

    return True


x = init('teste', '33019177000', '04', [2])
if x == None:
    print('sem notas')