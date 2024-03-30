from conf_banco import Banco

banco = Banco()

def verifica_credenciais(usuario, senha):
    user = banco.verificaUser(usuario)
    return user and senha == user[2]

def fazer_reserva(reserva_info):
    global projetores_disponiveis, caixas_som_disponiveis
    usuario = reserva_info['usuario']
    sala_id = reserva_info['sala_id']
    data_inicio = reserva_info['data_inicio']
    duracao = reserva_info['duracao']
    projetor = reserva_info['projetor']
    caixa_som = reserva_info['caixa_som']
    if projetor and projetores_disponiveis <= 0:
        return False, 'Recursos esgotados para projetor'
    if caixa_som and caixas_som_disponiveis <= 0:
        return False, 'Recursos esgotados para caixa de som'
    # Outras verificações...
    # Se todas as verificações passarem, faça a reserva no banco de dados
    try:
        banco.fazer_reserva(sala_id, data_inicio, duracao, usuario)
    except Exception as e:
        return False, f'Erro ao fazer reserva: {e}'
    return True, f"Parabéns, sua reserva foi realizada."

# Outras funções relacionadas ao seu aplicativo podem ser adicionadas aqui
