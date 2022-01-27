
# import mariadb
import mysql.connector as mysql

from conexao import conexao


class DB:
	def __init__(self):
		self.con= mysql.connect(**conexao)
		self.cursor= self.con.cursor(dictionary=True)
	def commit(self):
		self.con.commit()

# MAIN

db = DB()

try:
 db.cursor.execute("DROP TABLE GrupoFleury_Exames_4")
except:
 print("Tabela não existe - OK, será criada")

sqlcriatab = '''
CREATE TABLE hds.GrupoFleury_Exames_4
    ( id INT NOT NULL AUTO_INCREMENT ,
    ID_PACIENTE VARCHAR(50) NOT NULL ,
    ID_ATENDIMENTO VARCHAR(50) NOT NULL ,
    DT_COLETA DATE NOT NULL ,
    DE_ORIGEM VARCHAR(20) NOT NULL ,
    DE_EXAME VARCHAR(50) NOT NULL ,
    DE_ANALITO VARCHAR(50) NOT NULL ,
    DE_RESULTADO VARCHAR(30) NOT NULL ,
    CD_UNIDADE VARCHAR(20) NOT NULL ,
    DE_VALOR_REFERENCIA VARCHAR(30) NOT NULL ,
    PRIMARY KEY (id)) ENGINE = InnoDB;
    '''

try:
 db.cursor.execute(sqlcriatab)
except:
 print("ERRO - criação da tabela")

i = 0
with open('GrupoFleury_Exames_4.csv', 'r', encoding='utf-8') as infile:
    linha = infile.readline() # descarta primeira linha
    while True:
        linha = infile.readline()
        if linha=='': break
        i+=1
        p = linha.strip().split('|')
        if len(p)<9: continue
        q=[]
        for r in p:
            q.append(r.replace('"','\\"'))  # transforma " para \" em todos os campos
        sqlins = '''INSERT INTO GrupoFleury_Exames_4
            VALUES (NULL,"%s","%s","%s","%s","%s","%s","%s","%s","%s")
            '''%(q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7],q[8])
        try:
            db.cursor.execute(sqlins)
            if i%1000==0: 
                print(str(i))
                db.commit()
        except  mysql.Error as e:
            print("ERRO - inserção de dado "+linha+"\n"+str(e))

