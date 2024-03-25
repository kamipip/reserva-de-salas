import flask
import pytest
from unittest.mock import patch
from conf_banco import Banco
from main import login

class TestLogin:
    def test_login_with_correct_credentials(self):
        # Mock the request object
        with patch('flask.request') as request:
            request.method = 'POST'
            request.form = {'username': 'correct_username', 'password': 'correct_password'}
        
            # Mock the Banco.verificaUser() method
            with patch.object(Banco, 'verificaUser') as verificaUser:
                verificaUser.return_value = ('correct_username', 'correct_password')
        
                with patch('flask.session') as session:
                    login()
        
                    assert session['usuario_logado'] == 'correct_username'
                    flask.redirect.assert_called_once_with(flask.url_for('home'))

    def test_login_with_empty_fields(self):
        with patch('flask.request') as request:
            request.method = 'POST'
            request.form = {'username': '', 'password': ''}
        
            response = login()
        
            assert 'Usuario ou senha incorretos, tente novamente.' in response.get_data(as_text=True)
            flask.render_template.assert_called_once_with('index.html')

if __name__ == '__main__':
    pytest.main()
