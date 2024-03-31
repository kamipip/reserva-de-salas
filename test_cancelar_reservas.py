import unittest
from unittest.mock import patch, MagicMock
from main import app

class TestCancelarReservaFormulario(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    # Teste quando o usuário está logado
    def test_cancelar_reserva_usuario_logado(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['usuario_logado'] = 'usuario_teste'

            # Simulando uma requisição POST com o id da reserva
            response = client.post('/cancelar-reserva', data={'reserva_id': 1})

            # Verifica se a resposta é um JSON com a mensagem de sucesso
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Reserva cancelada com sucesso', response.data)

    # Teste quando o usuário não está logado
    def test_cancelar_reserva_usuario_nao_logado(self):
        with self.app as client:
            # Simulando uma requisição POST sem usuário logado
            response = client.post('/cancelar-reserva', data={'reserva_id': 1})

            # Verifica se a resposta é um JSON com a mensagem de erro
            self.assertEqual(response.status_code, 401)
            self.assertIn('Usuário não está logado'.encode(), response.data)



    # Teste quando ocorre um erro durante a remoção da reserva do banco de dados
    @patch('main.banco.conectaBanco')
    def test_cancelar_reserva_erro_banco(self, mock_conecta_banco):
        # Configura o mock para retornar uma exceção durante a remoção da reserva
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Erro no banco de dados')
        mock_conecta_banco.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        with self.app as client:
            with client.session_transaction() as sess:
                sess['usuario_logado'] = 'usuario_teste'

            # Simulando uma requisição POST com o id da reserva
            response = client.post('/cancelar-reserva', data={'reserva_id': 1})

            # Verifica se a resposta é um JSON com a mensagem de erro
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'Erro ao cancelar reserva', response.data)

if __name__ == '__main__':
    unittest.main()
