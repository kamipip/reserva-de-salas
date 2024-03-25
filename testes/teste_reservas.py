import pytest
from main import reserva
from flask import jsonify

@pytest.mark.parametrize("method, expected_result", [
    ('POST', "Parabéns, sua reserva foi realizada. Não esqueça que foi para o dia 01 de janeiro de 2022 e por apenas 2 horas."),
    ('GET', jsonify({'message': 'Usuário não está logado'}), 401)
])
def test_reserva(method, expected_result, mocker):
    mocker.patch.dict('main.session', {'usuario_logado': 'user123'})
    mocker.patch('main.request', method=method)

    result = reserva()

    assert result == expected_result
