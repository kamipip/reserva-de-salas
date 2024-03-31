import flask
import pytest
from unittest.mock import patch, MagicMock  # Importe MagicMock
from conf_banco import Banco
from main import login, app  # Importe a variável de aplicativo app
from flask import request

class TestLogin:
    def test_login_with_correct_credentials(self):
        # Mock the Banco.verificaUser() method
        with patch.object(Banco, 'verificaUser') as verificaUser:
            verificaUser.return_value = ('usuarioteste', 'senha123')
            
            # Mock the session object
            with app.test_request_context('/'):  # Crie um contexto de solicitação com o aplicativo Flask
                with patch('main.session') as session:
                    session.__getitem__.return_value = 'usuarioteste'  # Simule o valor do usuário logado
                    # Mock flask.url_for() to return a value
                    flask.url_for = MagicMock(return_value='/home')
                    
                    response = login()
                    assert session['usuario_logado'] == 'usuarioteste'
                    assert response == '/home'

    def test_login_with_empty_fields(self):
        # Mock the request object
        with app.test_request_context('/'):  # Crie um contexto de solicitação com o aplicativo Flask
            with patch('main.request') as request:
                request.method = 'POST'
                request.form = {'username': '', 'password': ''}
                
                response = login()
                
                assert 'Usuario ou senha incorretos, tente novamente.' in response
                assert response.status_code == 200
                assert flask.render_template.called_once_with('index.html')

if __name__ == '__main__':
    pytest.main()
