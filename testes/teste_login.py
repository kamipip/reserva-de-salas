    # Login com user e senha corretos
import flask

from conf_banco import Banco
from main import login


def test_login_with_correct_credentials(self, mocker):
        # Mock the request object
        mocker.patch('flask.request')
        flask.request.method = 'POST'
        flask.request.form = {'username': 'correct_username', 'password': 'correct_password'}
    
        # Mock the banco.verificaUser() method
        mocker.patch.object(Banco, 'verificaUser')
        Banco.verificaUser.return_value = ('correct_username', 'correct_password')
    
        mocker.patch('flask.session')
    
        login()
    
        assert flask.session['usuario_logado'] == 'correct_username'
        assert flask.redirect.called_with(flask.url_for('home'))
            # Login with empty username and password fields
def test_login_with_empty_fields(self, mocker):
        
        mocker.patch('flask.request')
        flask.request.method = 'POST'
        flask.request.form = {'username': '', 'password': ''}
    
        response = login()
    
        assert 'Usuario ou senha incorretos, tente novamente.' in response.get_data(as_text=True)
        assert flask.render_template.called_with('index.html')