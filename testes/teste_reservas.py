    # Retorna uma mensagem de sucesso quando uma reserva é feita com dados válidos
from ast import main

from flask import jsonify


def test_success_message(self, mocker):
        # Mocking da sessão
        mocker.patch.dict('main.session', {'usuario_logado': 'user123'})

        # Mocking o pedido
        mocker.patch('main.request', method='POST', form={'sala': '1', 'data_inicio': '2022-01-01T10:00', 'duracao': '2', 'usuario': 'user123'})

        # Mocking a conexão do banco de dados e o cursor
        mock_db = mocker.MagicMock()
        mock_cursor = mocker.MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mocker.patch('main.banco.conectaBanco', return_value=mock_db)

        # Mocking ele executa o método do cursor
        mock_cursor.fetchone.return_value = None

        # Chamando a função em teste
        result = main.reserva()

        
        assert result == "Parabéns, sua reserva foi realizada. Não esqueça que foi para o dia 01 de janeiro de 2022 e por apenas 2 horas."

            # Retorna uma mensagem de erro quando o método de solicitação não é POST
def test_error_message(self, mocker):
        # Mocking a sessão
        mocker.patch.dict('main.session', {'usuario_logado': 'user123'})

        # Mocking o pedido
        mocker.patch('main.request', method='GET')

        # Chamando a função do teste
        result = main.reserva()

        
        assert result == jsonify({'message': 'Usuário não está logado'}), 401