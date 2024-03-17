    # Cancela uma reserva com sucesso quando recebe um ID de reserva válido e o usuário está conectado
import flask

from main import cancelar_reserva


def test_cancelar_reserva_valid_id_logged_in(self, mocker):
        # Mocking the session
        mocker.patch.dict('flask.session', {'usuario_logado': 'user123'})

        # Mocking the request
        mocker.patch('flask.request')
        flask.request.form = {'reserva_id': '123'}

        # Mocking a conexão do banco de dados e o cursor
        mock_db = mocker.MagicMock()
        mock_cursor = mocker.MagicMock()
        mock_db.cursor.return_value = mock_cursor

        # Mocking os métodos execute e commit
        mock_cursor.execute.return_value = None
        mock_db.commit.return_value = None

        
        response = cancelar_reserva()
        
        assert response == flask.jsonify({'message': 'Reserva cancelada com sucesso'})
        mock_cursor.execute.assert_called_once_with("DELETE FROM reservas WHERE id = %s", ('123',))
        mock_db.commit.assert_called_once()

    # Retorna uma mensagem JSON com erro quando o usuário não está logado
def test_cancelar_reserva_not_logged_in(self, mocker):
        # Mock session
        mocker.patch.dict('flask.session', {'usuario_logado': None})

        # chama a função
        result = cancelar_reserva()

        assert result == {'message': 'Usuário não está logado'}
        assert flask.jsonify.called_with({'message': 'Usuário não está logado'}), 401