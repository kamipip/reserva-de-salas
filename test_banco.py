from datetime import datetime
import unittest
from main import Banco

class TestBanco(unittest.TestCase):

    def setUp(self):
        self.banco = Banco()

    def tearDown(self):
        pass

    def test_verificaUser(self):
        resultado = self.banco.verificaUser('usuarioteste')
        self.assertEqual(resultado, (4, 'usuarioteste', 'senha123', 'usuarioteste'))

    def test_obterSalas(self):
        resultado = self.banco.obterSalas()
        self.assertEqual(resultado, ['sala 01', 'sala 02', 'sala 03'])

    def test_obterReservasUsuario(self):
        resultado = self.banco.obterReservasUsuario('usuarioteste')
        self.assertEqual(resultado, [(18, 'sala 01', datetime(2024, 4, 1, 10, 0), 1)])

    def test_obterSalaPorNome(self):
        resultado = self.banco.obterSalaPorNome('sala 01')
        self.assertEqual(resultado, 1)

if __name__ == '__main__':
    unittest.main()
