import mysql.connector


class Banco:
    def __init__(self):
        self.conexao = self.conectaBanco()


    def conectaBanco(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="gerencia"
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


    def obterReservasUsuario(self, usuario):
        try:
            print("Usuário recebido:", usuario)  # Verifica se o usuário está sendo passado corretamente
            with self.conectaBanco() as mydb:
                cursor = mydb.cursor()
                cursor.execute("SELECT r.id, s.nome, r.data_inicio, r.duracao FROM reservas r INNER JOIN salas s ON r.sala_id = s.id WHERE usuario = %s", (usuario,))
                reservas = cursor.fetchall()
            print("Reservas do usuário:", reservas)  # Verifica se as reservas foram recuperadas corretamente
            return reservas
        except Exception as e:
            print("Erro ao obter as reservas do usuário:", e)
            return None
        
    def obterSalaPorNome(self, nome_sala):
        try:
            with self.conectaBanco() as mydb:
                cursor = mydb.cursor()
                cursor.execute("SELECT id FROM salas WHERE nome = %s", (nome_sala,))
                sala = cursor.fetchone()
            if sala:
                return sala[0]
            else:
                return None
        except Exception as e:
            print("Erro ao obter sala por nome:", e)
            return None
