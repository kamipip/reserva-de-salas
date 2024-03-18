import mysql.connector

class Banco:
    def __init__(self):
        self.conexao = self.conectaBanco()

    def conectaBanco(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="gerencia-salas"
        )

    def verificaUser(self, usuario):
        with self.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM acesso WHERE user = %s", (usuario,))
            resultado = cursor.fetchone()
            return resultado

    def obterSalas(self):
        with self.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT nome FROM salas")
            salas = [sala[0] for sala in cursor.fetchall()]
        return salas

