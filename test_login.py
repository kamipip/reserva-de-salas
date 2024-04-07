import pytest
from unittest.mock import patch 
from conf_banco import Banco
from main import login, app 

class TestLogin:
    def test_login_with_correct_credentials(self):
        with patch.object(Banco, 'verificaUser') as verificaUser:
            verificaUser.return_value = (1, 'usuarioteste', 'senha123', 'Nome do Usuário')

            # Simula uma solicitação POST para a rota de login
            with app.test_client() as client:
                response = client.post('/login', data={'username': 'usuarioteste', 'password': 'senha123'}, follow_redirects=True)
                
                # Verifica se o redirecionamento ocorreu corretamente para a página 'home'
                assert response.status_code == 200  
                assert b'<title>Inicio</title>' in response.data  # Verifica se a página 'home' foi renderizada
    
    def test_login_with_empty_fields(self):
        with app.test_request_context('/'):
            with patch('main.request') as request:
                request.method = 'POST'
                request.form = {'username': '', 'password': ''}
                response = login()
                assert 'Usuario ou senha incorretos, tente novamente.' in response  # Verifica a mensagem de erro

if __name__ == '__main__':
    pytest.main()
