from unittest.mock import patch
from flask import render_template
import pytest


def test_user_has_reservations(mocker):
    
    from main import minhas_reservas
   
    mocker.patch('flask.session', {'usuario_logado': 'user123'})

    with patch('main.banco.obterReservasUsuario', return_value=['reserva1', 'reserva2']):

        response = minhas_reservas()

    assert len(response) == 2 

    assert response == render_template('minhas_reservas.html', reservas=['reserva1', 'reserva2'])

if __name__ == "__main__":
    pytest.main()
