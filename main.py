from contextlib import contextmanager
from contextlib import closing
from pymysql import connect
from pymysql.cursors import DictCursor


@contextmanager
def closing(conexao):
    try:
        yield conexao
    finally:
        conexao.close()

def openClose(fun):
    def run(sql=None):
        coon =connect(host='localhost' ,port=3306 ,user='root', password='1234qwer', db='test', charset='utf8')
        cursor = coon.cursor()
        try:
            cursor.execute(fun( sql))
            data = cursor.fetchall()
            coon.commit()
            print(data)
        except Exception as e:
            coon.rollback()
            print ( 'run', str (fun), 'error when the method, the error code:', e)
        finally:
            cursor.close()
            coon.close()
    return run

@openClose
def runSql(sql=None):
    if sql is None:
        sql = 'select * from students1'
    return sql
runSql()
runSql(‘select * from students1‘ where name= ‘tom1’)

def criatabela():
    with closing(connect(host='localhost', user='root', database='bot', password='1230', cursorclass=DictCursor)) as con:
        with closing(con.cursor()) as c:
            sql = 'CREATE TABLE lojas (id INT AUTO_INCREMENT PRIMARY KEY, Nome VARCHAR(30) NOT NULL, id_user VARCHAR(30) NOT NULL, Lj1 BIT DEFAULT(0) NOT NULL, Lj2 BIT DEFAULT(0) NOT NULL, \
            Lj3 BIT DEFAULT(0) NOT NULL, Lj4 BIT DEFAULT(0) NOT NULL, Lj5 BIT DEFAULT(0) NOT NULL, Lj6 BIT DEFAULT(0) NOT NULL, Lj7 BIT DEFAULT(0) NOT NULL, Pdf BIT DEFAULT(0) NOT NULL)'
            c.execute(sql)


def checa_id(id_user0):
    with closing(connect(host='localhost', user='root', database='bot', password='1230', cursorclass=DictCursor)) as con:
        with closing(con.cursor()) as c:
            sql = f'SELECT id_user FROM lojas WHERE id_user = {str(id_user0)}'
            c.execute(sql)
            resultado = c.fetchone()  #Retorna todos os items obtidos pela consulta na tabela
            if id_user0 == resultado['id_user']:
                return True
            else:
                return False


def salva_banco(nome, id_, escolhas):
    if not checa_id(id_):
        with closing(
                connect(host='localhost', user='root', database='bot', password='1230', cursorclass=DictCursor)) as con:
            with closing(con.cursor()) as c:
                sql = f'INSERT INTO lojas (nome, id_user, {escolhas}) VALUES (%s,%s,%s)'
                dados = (nome, id_, 1)
                c.execute(sql, dados)
                con.commit()  #Lança as alterações no BD
    else:
        edita_banco(nome, id_, escolha)


def edita_banco(nome, id_, escolha):
    with closing(
            connect(host='localhost', user='root', database='bot', password='1230', cursorclass=DictCursor)) as con:
        with closing(con.cursor()) as c:
            sql = f'ALTER TABLE lojas (nome, id_user, {escolha}) VALUES (%s,%s,%s)'
            dados = (nome, id_, 1)
            c.execute(sql, dados)
            con.commit()  # Lança as alterações no BD



print(checa_id("00"))
