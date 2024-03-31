# API de Reservas de Salas

## Visão Geral
A API de Reservas de Salas tem como objetivo fornecer um sistema eficiente para agendamento de salas de reunião e recursos associados. O sistema permitirá aos usuários visualizar as salas, fazer reservas e cancelar reservas existentes.

## Funcionalidades Principais
- **Reserva de Sala de Reunião:** Os usuários podem agendar uma sala de reunião especificando a data, hora e duração da reserva, bem como recursos adicionais necessários.
- **Cancelamento de Reserva:** Os usuários podem cancelar uma reserva existente, se associada a sua conta.
- **Adição de Recursos Extras:** Os usuários terão a opção de adicionar recursos extras às suas reservas, como projetores ou equipamentos de áudio, para atender às necessidades específicas de sua reunião.


## Tecnologias Utilizadas
- **Linguagem de programação:** Python
- **Framework web:** Flask
- **Banco de dados:** MySQL
- **Interface:** HTML, CSS
- **Framework de design:** Bootstrap


Para rodar o projeto, você deve usar o comando `python main.py` no seu terminal e acessar a porta [http://localhost:5000](http://localhost:5000).


# TESTES

# Objetivo dos Testes

Este repositório contém testes para uma aplicação de login em Flask, com mocks para testar diferentes cenários de autenticação.

## Como Usar os Testes

Para executar os testes, é necessário ter o Python e o framework pytest instalados no sistema. Utilize o seguinte comando:

```bash
pytest test_modulo.py
```

# Testes de Unidade para Classe Login

1. **main.py**: Contém a lógica principal da aplicação, incluindo a função de login.
2. **conf_banco.py**: Arquivo de configuração do banco de dados, contendo a classe `Banco` com métodos para verificação de usuários.
3. **test_login.py**: Arquivo de teste com casos de teste para a função de login.

## Descrição dos Testes

test_login_with_correct_credentials: Testa o login com credenciais corretas. Mocks são utilizados para simular a verificação do usuário no banco de dados e para simular a sessão do Flask. O objetivo é garantir que o usuário seja redirecionado para a página inicial após o login bem-sucedido.

test_login_with_empty_fields: Testa o login com campos vazios. Um mock é usado para simular a requisição do Flask com campos de formulário vazios. O objetivo é garantir que a mensagem de erro correta seja exibida ao tentar fazer login com campos vazios.

# Testes de Unidade para Classe Banco

Este repositório contém testes de unidade para a classe `Banco`, que é responsável por interagir com um banco de dados fictício em um sistema de reservas de salas. Os testes cobrem diferentes métodos da classe `Banco` para garantir que eles estejam funcionando conforme o esperado.

## Descrição dos Testes

1. **test_verificaUser**: Testa o método `verificaUser` da classe `Banco`. Este método verifica se um usuário está presente no banco de dados e retorna suas informações. O teste verifica se as informações retornadas para um usuário existente correspondem às esperadas.

2. **test_obterSalas**: Testa o método `obterSalas` da classe `Banco`. Este método retorna uma lista de salas disponíveis no sistema. O teste verifica se a lista retornada corresponde às salas esperadas.

3. **test_obterReservasUsuario**: Testa o método `obterReservasUsuario` da classe `Banco`. Este método retorna as reservas feitas por um usuário específico. O teste verifica se as reservas retornadas para um usuário existente correspondem às esperadas.

4. **test_obterSalaPorNome**: Testa o método `obterSalaPorNome` da classe `Banco`. Este método retorna o ID de uma sala com base no nome fornecido. O teste verifica se o ID retornado para uma sala existente corresponde ao esperado.

# Testes para Cancelamento de Reserva - Formulário

Este repositório contém testes para a funcionalidade de cancelamento de reservas em um sistema web. Os testes são realizados utilizando a biblioteca unittest do Python e mocks para simular o comportamento do banco de dados e do ambiente de execução.

## Descrição dos Testes

1. **test_cancelar_reserva_usuario_logado**: Testa o cancelamento de reserva quando o usuário está logado. Simula uma requisição POST com o ID da reserva e verifica se a resposta é um JSON com a mensagem de sucesso "Reserva cancelada com sucesso".

2. **test_cancelar_reserva_usuario_nao_logado**: Testa o cancelamento de reserva quando o usuário não está logado. Simula uma requisição POST sem usuário logado e verifica se a resposta é um JSON com a mensagem de erro "Usuário não está logado" e o status code 401 (Unauthorized).

3. **test_cancelar_reserva_erro_banco**: Testa o cenário em que ocorre um erro durante a remoção da reserva do banco de dados. Utiliza um mock para simular a conexão com o banco de dados e configura-o para retornar uma exceção durante a remoção da reserva. Verifica se a resposta é um JSON com a mensagem de erro "Erro ao cancelar reserva" e o status code 500 (Internal Server Error).

# Testes para Minhas Reservas

Este repositório contém testes para a funcionalidade de visualização das reservas do usuário em um sistema web. Os testes são realizados utilizando a biblioteca unittest do Python e mocks para simular o ambiente de execução.

## Descrição dos Testes

1. **test_minhas_reservas_no_user_logged_in**: Testa a visualização das reservas quando nenhum usuário está logado. Simula uma requisição GET para a rota '/minhas-reservas' e verifica se a resposta é um redirecionamento (código de status 302).

## Requisitos

Python 3.x instalado no seu sistema.
pytest instalado no seu ambiente de desenvolvimento.
