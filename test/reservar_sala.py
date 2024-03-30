# reservar_sala.py

class BancoDeDados:
    def __init__(self):
        # Simulando dados do banco de dados
        self.usuarios = {
            'user1': {'senha': 'senha1', 'nome': 'Usuário 1'},
            'user2': {'senha': 'senha2', 'nome': 'Usuário 2'},
            'user3': {'senha': 'senha3', 'nome': 'Usuário 3'},
        }

        self.reservas = []

    def verificar_credenciais(self, usuario, senha):
        if usuario in self.usuarios and self.usuarios[usuario]['senha'] == senha:
            return True, self.usuarios[usuario]['nome']
        else:
            return banco.verificar_credenciais(usuario, senha)[0]  # Retorna apenas o primeiro valor da tupla, que é True ou False


    def reserva_sala(self, sala_id, data_inicio, duracao, usuario):
        # Aqui você pode adicionar lógica para verificar a disponibilidade da sala, conflitos de horário, etc.
        # Por enquanto, vamos apenas adicionar a reserva à lista de reservas simulada.
        self.reservas.append({
            'sala_id': sala_id,
            'data_inicio': data_inicio,
            'duracao': duracao,
            'usuario': usuario
        })
        return True


banco = BancoDeDados()

def verifica_credenciais(usuario, senha):
    return banco.verificar_credenciais(usuario, senha)

def fazer_reserva(reserva_info):
    return banco.reserva_sala(**reserva_info)
