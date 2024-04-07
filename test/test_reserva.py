import unittest
from unittest.mock import MagicMock, patch
from reservar_sala import verifica_credenciais, fazer_reserva

class TestAuthentication(unittest.TestCase):

    @patch('reservar_sala.banco.verificar_credenciais')
    def test_verifica_credenciais(self, mock_verificar_credenciais):

        mock_verificar_credenciais.return_value = (True, 'Test User')
        self.assertTrue(verifica_credenciais('test_user', 'hashed_password')) # Testa credenciais válidas
        mock_verificar_credenciais.return_value = (False, None)
        resultado, _ = verifica_credenciais('test_user', 'wrong_password') # Testa credenciais inválidas
        
        self.assertFalse(resultado)

class TestReservation(unittest.TestCase):

    @patch('reservar_sala.banco.reserva_sala')
    def test_fazer_reserva_com_projetor_disponivel(self, mock_reserva_sala):

        mock_reserva_sala.return_value = True

        # Testa fazer reserva com sucesso
        reserva_info = {
            'sala_id': 'sala_teste',
            'data_inicio': '2024-03-30T09:00',
            'duracao': '2',
            'usuario': 'test_user',
            'projetor': 'on',
            'caixa_som': None
        }
        resultado = fazer_reserva(reserva_info)
        self.assertTrue(resultado)

    @patch('reservar_sala.banco.reserva_sala')
    def test_fazer_reserva_com_projetor_esgotado(self, mock_reserva_sala):
        mock_reserva_sala.return_value = False

        # Testa fazer reserva com falha
        reserva_info = {
            'sala_id': 'sala_teste',
            'data_inicio': '2024-03-30T09:00',
            'duracao': '2',
            'usuario': 'test_user',
            'projetor': 'on',
            'caixa_som': None
        }
        resultado = fazer_reserva(reserva_info)
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()
