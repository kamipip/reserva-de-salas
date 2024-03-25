import flask
import pytest
from unittest.mock import patch
from main import cancelar_reserva

class TestCancelarReserva:
    @pytest.mark.parametrize("usuario_logado", [None, 'user123'])
    @patch('flask.request')
    @patch.dict('flask.session')
    @patch('main.banco.conectaBanco')
    def test_cancelar_reserva(self, mock_conectaBanco, mock_session, mock_request, usuario_logado):
        mock_session.__getitem__.return_value = usuario_logado
        mock_request.form = {'reserva_id': '123'}

        mock_db = mock_conectaBanco.return_value.__enter__.return_value
        mock_cursor = mock_db.cursor.return_value

        response = cancelar_reserva()

        if usuario_logado is None:
            assert response == {'message': 'Usuário não está logado'}
        else:
            assert response == flask.jsonify({'message': 'Reserva cancelada com sucesso'})

        mock_cursor.execute.assert_called_once_with("DELETE FROM reservas WHERE id = %s", ('123',))
        mock_db.commit.assert_called_once()

if __name__ == '__main__':
    pytest.main()
