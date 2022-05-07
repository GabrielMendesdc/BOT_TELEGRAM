from os import listdir, path
import xml.etree.ElementTree as ET
from re import search


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
        set_nota = {'nNF', 'dhEmi', 'dhSaiEnt', 'xFant'}

        set_prod = {'xProd', 'CFOP', 'vProd', 'cEANTrib', 'cEAN', 'uCom', 'uTrib', 'qCom',
                    'qTrib', 'vDesc', 'vICMSST', 'vFCPST', 'vIPI', 'infAdProd'}

        zeros = {'0.0', '0.00', '0.000'}
        for i in self.caminho:
            arvore = ET.parse(i)
            raiz = arvore.getroot()
            for filho in raiz.iter():
                if filho.tag[36:] in set_nota:
                    self.info[filho.tag[36:]] = filho.text
                if filho.tag[36:] == 'det':
                    digitos = filho.attrib['nItem']
                    if prod:
                        prod.cfop()
                        self.produtos.append(prod)
                    prod = Produto(digitos, self.info['xFant'])
                if filho.tag[36:] == 'total':
                    prod.cfop()
                    self.produtos.append(prod)
                if filho.tag[36:] in set_prod:
                    if filho.text and filho.text not in zeros:
                        prod.info[filho.tag[36:]] = filho.text
                # self.produtos.append()
        # print(self.produtos)


class Produto:
    def __init__(self, index, xfant):
        self.index = index
        self.info = {'xFant': xfant}
        self.lista_boni = {'5910', '5911', '5912', '5912', '5913', '5914', '5915', '5916', '5917', '5918', '5919',
                           '1201', '1202', '1203', '1204', '1208', '1209', '1212', '1410', '1411', '1503', '1504',
                           '1505', '1506', '1553', '1660', '1661', '1662', '1918', '1919', '2201', '2202', '2203',
                           '2204', '2208', '2209', '2212', '2410', '2411', '2503', '2504', '2505', '2506', '2553',
                           '2660', '2661', '2662', '2918', '2919', '5201', '5202', '5208', '5209', '5210', '5410',
                           '5411', '5412', '5413', '5503', '5553', '5555', '5556', '5660', '5661', '5662', '5918',
                           '5919', '5921', '6201', '6202', '6208', '6209', '6210', '6410', '6411', '6412', '6413',
                           '6503', '6553', '6555', '6556', '6660', '6661', '6662', '6918', '6919', '6921', '7201',
                           '7202', '7210', '7211', '7212', '7553', '7556'}

        self.unidades = {'und', 'uns', 'uni', 'pct', 'frs', 'kgs', 'qts', 'qtd',
                         'grs', 'lat', 'lt', 'pa', 'cp', 'pt', 'pec'}

    def __repr__(self):
        return f'ID {self.index} info: {self.info}\n'

    def cfop(self):
        try:
            if self.info['CFOP']:
                pass
        except KeyError:
            return 0
        if self.info['CFOP'] in self.lista_boni:
            self.info['boni'] = True
        del self.info['CFOP']
        qtd = self.preco_final()
        self.precifica(qtd)

    def precifica(self, qtd):
        if not qtd:
            qtd = 1
        qtd_final = float(qtd) * float(self.info['qTrib']) #Tambem * qCom
        set_poe_zero = {'vProd', 'vICMSST', 'vFCPST', 'vIPI', 'vDesc', 'infAdProd'}
        for i in set_poe_zero:
            if i not in self.info.keys():
                self.info[i] = 0
            else:
                try:
                    self.info[i] = float(self.info[i])
                except ValueError:
                    pass
        self.info['preco'] = round((float(self.info['vProd'] + self.info['vICMSST'] + self.info['vFCPST']
                    + self.info['vIPI'] - self.info['vDesc']) / qtd_final), 2)
        exclusao = {'xFant', 'cEANTrib', 'cEAN', 'uCom', 'uTrib', 'qCom', 'qTrib', 'vProd',
                    'vIPI', 'vFCPST', 'vICMSST', 'vDesc', 'infAdProd'}
        for i in exclusao:
            del self.info[i]
        print(self.info)

    def preco_final(self):
        # ean = checkean(self.info['cEANTrib'])
        # if ean:
        #     print('cEANTrib', self.info['cEANTrib'])
        #     return ean
        # else:
        #     ean = checkean(self.info['cEAN'])
        #     if ean:
        #         print('cEAN', self.info['cEAN'])
        #         return ean

        if self.info['xFant'] == 'MARSIL' or self.info['xFant'].startswith('NOVA CAMPINAS'):
            return pega_qtd_x(self.info['xProd'], self.info['xFant'])

        # if self.info['uTrib'] == self.info['uCom'] and not self.info['uTrib'].isalpha():
            # return self.info['qTrib'] #ex: CX24, cx36...

        # elif self.info['uTrib'] == self.info['uCom'] and not self.info['uCom'].isalpha():
        #     return self.info['qCom']

        if self.info['uTrib'] == self.info['uCom'] and self.info['qTrib'] == self.info['qCom'] and \
           self.info['uTrib'].upper() == 'UN':
            return 1

        if self.info['uTrib'] == self.info['uCom']:
            lista_res = [i for i in self.unidades if search(self.info['uTrib'], i.upper())]
            if lista_res:
                return 1
        else:
            return pega_qtd_x(self.info['xProd'], self.info['xFant'])


def busca_xmls(cnpj, mes, loja, numero):
    lojas = [0, '05349537000185', '07246178000166', '08158815000105', '32265622000138',
             '05349537000266', '23017342000209', '23017342000110']

    ljs = [lojas[int(i)] for i in loja]
    arq = []
    for lj in ljs:
        dire = path.join('N:\\', 'XML ENTRADA', 'destinadas', lj, f'2022-{mes}')
        print(dire)
        if cnpj:
            arq.append([path.join(dire, f) for f in listdir(dire) if str(cnpj) in f])
        else:
            arq.append([path.join(dire, f) for f in listdir(dire) if str(numero) in f])
    return arq


def checkean(ean):
    ean = str(ean)
    if len(ean) > 13:
        ean = ean[1:]
    with open("C:\\Users\\pdv\\projetos_jupyter\\txte.txt", 'r') as db:
        for linha in db:
            if linha[:13] == ean[:13]:
                return linha[15:]


def pega_qtd_x(string, xfant):
    esquerda = []
    direita = []
    passei = False
    padrao = string.split(' ')[-1].lower()
    string = ''.join(string.split(' ')[0:-1])

    if xfant == 'MARSIL':
        padrao = [i.lower() for i in string.split(' ') if 'x' in i.lower()][0]
        if padrao.startswith('cx'):
            return int(''.join(i for i in padrao if i.isdigit()))
    for i in padrao:
        if i != 'x' and not passei:
            esquerda.append(i)
        if i == 'x':
            passei = True
        if passei and i != 'x':
            direita.append(i)
    direita = ''.join(i for i in direita)
    esquerda = ''.join(i for i in esquerda)
    if direita.isdigit() and direita.isdigit():
        if direita not in string and esquerda in string:
            return direita
        elif esquerda not in string and direita in string:
            return esquerda
        else:
            if float(direita) > float(esquerda):
                return direita
            else:
                return esquerda
    if direita.isdigit():
        return direita
    if esquerda.isdigit():
        return esquerda
    return 1


def init(id_, cnpj, mes, loja, numero=0):
    usuario = User(id_)
    notas = busca_xmls(cnpj, mes, loja, numero)
    if not notas:
        return None
    print(notas)
    usuario.add_notas(notas)

    return True


x = init('teste', '14450629', '05', [1, 2])
if not x:
    print('sem notas')
