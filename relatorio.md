# Sistema de Reservas de Salas

O projeto visa desenvolver um sistema eficiente para agendamento de salas de reunião e recursos associados. O sistema permitirá aos usuários visualizar as salas, fazer reservas e cancelar reservas existentes.

## Visão geral das funcionalidades:

1. **Visualização da Disponibilidade das Salas:** Os usuários poderão visualizar a disponibilidade das salas de reunião em um determinado período, permitindo que planejem suas reuniões com antecedência.

2. **Reserva de Salas:** Os usuários poderão escolher entre as salas disponíveis e reservar uma delas especificando a data, hora e duração da reserva. 

3. **Adição de Recursos Extras:** Os usuários terão a opção de adicionar recursos extras às suas reservas, como projetores ou equipamentos de áudio, para atender às necessidades específicas de sua reunião.

4. **Cancelamento de Reservas:** Os usuários poderão cancelar uma reserva existente caso não precisem mais da sala ou se houver mudanças nos planos da reunião.

## Tecnologias Utilizadas:

1. **Flask:** O sistema foi desenvolvido usando o framework Flask, que é uma estrutura leve e flexível para o desenvolvimento de aplicativos web em Python. Flask oferece facilidade de uso e extensibilidade, permitindo a criação de aplicativos web poderosos e escaláveis.

2. **MySQL:** O banco de dados MySQL foi utilizado para armazenar informações sobre salas, reservas e recursos adicionais. MySQL é um sistema de gerenciamento de banco de dados relacional confiável e amplamente utilizado, que oferece desempenho e segurança robustos.

3. **Bootstrap:** A interface do usuário foi desenvolvida usando Bootstrap, um framework front-end de código aberto que facilita a criação de interfaces web responsivas e visualmente atraentes. Bootstrap oferece uma variedade de componentes e estilos pré-projetados que aceleram o desenvolvimento e garantem uma experiência de usuário consistente em diferentes dispositivos.

## Banco de Dados

O banco de dados utilizado no projeto foi criado da seguinte maneira:

```sql
CREATE DATABASE gerencia;
USE gerencia;

CREATE TABLE `acesso` (
  `id` int(11) NOT NULL,
  `user` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nome` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `salas` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `recursos` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `sala_id` int(11) NOT NULL,
  `data_inicio` datetime NOT NULL,
  `duracao` int(11) NOT NULL,
  `usuario` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


ALTER TABLE `acesso`
  MODIFY COLUMN `id` int(11) NOT NULL AUTO_INCREMENT,
  ADD PRIMARY KEY (`id`);

ALTER TABLE `salas`
  MODIFY COLUMN `id` int(11) NOT NULL AUTO_INCREMENT,
  ADD PRIMARY KEY (`id`);

ALTER TABLE `reservas`
  MODIFY COLUMN `id` int(11) NOT NULL AUTO_INCREMENT,
  ADD PRIMARY KEY (`id`); 
```


## Templates HTML

Para a interface do usuário, foram desenvolvidos os seguintes templates HTML:

- **index.html:** Corresponde à página de login, onde os usuários podem inserir suas credenciais para acessar o sistema.

- **reserva.html:** Permite aos usuários agendar uma nova reserva de sala de reunião. Ele exibe um formulário onde os usuários podem selecionar a sala desejada, a data e hora de início da reserva, a duração da reserva e opcionalmente adicionar recursos como projetores e caixas de som.

- **minhas_reservas.html:** Exibe as reservas existentes do usuário logado. Ele mostra uma lista das reservas feitas pelo usuário, incluindo informações como o nome da sala, a data de início da reserva e a duração.

- **pagina.html:** Corresponde à página principal do sistema após o login bem-sucedido. Ele exibe uma saudação ao usuário logado e uma lista das salas disponíveis para reserva.

## Interação com o banco de dados
Para interagir com o banco de dados MySQL, foram utilizadas as seguintes classes e métodos: 

O método __init__  estabelece uma conexão com o banco de dados chamando o método conectaBanco() e armazena essa conexão no atributo conexao.
```python
import mysql.connector

class Banco:
    def __init__(self):
        self.conexao = self.conectaBanco()
```
O método `conectaBanco` cria e retorna uma conexão com o banco de dados MySQL.
```python
    def conectaBanco(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="gerencia"
        )
```
O método `verificaUser` recebe o nome de usuário como argumento e verifica se esse usuário existe na tabela acesso. Ele executa uma consulta SQL para selecionar os dados do usuário especificado e retorna o resultado dessa consulta.

```python
    def verificaUser(self, usuario):
        with self.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM acesso WHERE user = %s", (usuario,))
            resultado = cursor.fetchone()
            return resultado
```

O método `obterSalas` obtém todos os nomes das salas disponíveis no banco de dados. Ele executa uma consulta SQL para selecionar os nomes das salas da tabela `salas` e retorna uma lista contendo esses nomes.
```python
    def obterSalas(self):
        with self.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT nome FROM salas")
            salas = [sala[0] for sala in cursor.fetchall()]
        return salas
```

O método `obterReservasUsuario` recebe o nome de usuário como argumento e retorna todas as reservas associadas a esse usuário. Ele executa uma consulta SQL para selecionar os dados das reservas feitas pelo usuário especificado, incluindo o ID da reserva, o nome da sala, a data de início e a duração. Se ocorrer algum erro durante a execução da consulta, ele imprime uma mensagem de erro e retorna None.

```python
    def obterReservasUsuario(self, usuario):
        try:
            with self.conectaBanco() as mydb:
                cursor = mydb.cursor()
                cursor.execute("SELECT r.id, s.nome, r.data_inicio, r.duracao FROM reservas r INNER JOIN salas s ON r.sala_id = s.id WHERE usuario = %s", (usuario,))
                reservas = cursor.fetchall()
            return reservas
        except Exception as e:
            print("Erro ao obter as reservas do usuário:", e)
            return None
```


## Funções do Arquivo main.py

### Função index
Redireciona os usuários para a página de login quando acessam o endpoint raiz do aplicativo.

```python
@app.route('/')
def index():
    return redirect(url_for('login'))
```

### Função login
Esta função trata das requisições de login. Quando a requisição é do tipo POST, verifica se as credenciais do usuário são válidas e, se forem, redireciona o usuário para a página inicial. Caso contrário, exibe uma mensagem de erro na página de login. Se a requisição for do tipo GET, exibe a página de login.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        user = banco.verificaUser(usuario)  
       
        if user and senha == user[2]:
            session['usuario_logado'] = user[3]
            return redirect(url_for('home'))
        else:
            error = 'Usuario ou senha incorretos, tente novamente.'
            return render_template('index.html', error=error)
    return render_template('index.html')
```

### Função home
Esta função verifica se o usuário está logado. Se não estiver, redireciona-o para a página de login. Se estiver logado, obtém o nome do usuário a partir da sessão e obtém a lista de salas disponíveis no banco de dados. Em seguida, renderiza a página 'pagina.html', passando o nome do usuário e a lista de salas como parâmetros.

```python
@app.route('/home')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    else:
        nome = session['usuario_logado']

        with banco.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM salas")
            salas = [sala[1] for sala in cursor.fetchall()]  # Apenas os nomes das salas

        return render_template('pagina.html', nome=nome, salas=salas)
```

### Função listar_salas
Esta função obtém a lista de salas disponíveis utilizando o método obterSalas do objeto banco e retorna a lista no formato JSON.

```python
def listar_salas():
    salas = banco.obterSalas()
    return jsonify(salas)
```

### Função reserva
Nesta primeira parte, foi definida a função reserva como uma rota no aplicativo Flask, que pode ser acessada através da URL /reserva. Ela aceita tanto solicitações GET quanto POST. A primeira verificação é se o usuário está logado. Se não estiver, uma mensagem de erro é retornada indicando que o usuário não está autorizado.
```python
@app.route('/reserva', methods=['GET', 'POST'])
def reserva():

    global projetores_disponiveis, caixas_som_disponiveis
   
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return jsonify({'message': 'Usuário não está logado'}), 401
```

Se a solicitação for do tipo POST, significa que o usuário está enviando um formulário para fazer uma reserva. Aqui, os dados do formulário são recuperados, incluindo o ID da sala, a data de início da reserva, a duração, o usuário que está fazendo a reserva e se recursos adicionais como projetor ou caixa de som foram solicitados.
```python
    if request.method == 'POST':
        sala_id = request.form['sala']
        data_inicio = request.form['data_inicio']
        duracao = request.form['duracao']
        usuario = request.form['usuario']
        projetor = request.form.get('projetor')  
        caixa_som = request.form.get('caixa_som')
```


Esta parte verifica se os recursos adicionais (projetor e caixa de som) foram solicitados e se estão disponíveis. Se algum dos recursos estiver esgotado, uma mensagem de erro é retornada. Depois, se os recursos adicionais forem solicitados e estiverem disponíveis, decrementamos a quantidade disponível desses recursos. Por fim, é verificado se a quantidade de recursos disponíveis é menor que zero após a atualização. Se for o caso, uma mensagem de erro é retornada, indicando uma quantidade inválida de recursos disponíveis.
```python       
        # Verificar se há recursos disponíveis
        if projetor and projetores_disponiveis <= 0:
            return jsonify({'message': 'Recursos esgotados para projetor'}), 400
        if caixa_som and caixas_som_disponiveis <= 0:
            return jsonify({'message': 'Recursos esgotados para caixa de som'}), 400
        # Atualizar a quantidade disponível de recursos
        if projetor:
            projetores_disponiveis -= 1
        if caixa_som:
            caixas_som_disponiveis -= 1
        # Verificar se a quantidade de recursos disponíveis não é menor que zero
        if projetores_disponiveis < 0 or caixas_som_disponiveis < 0:
            return jsonify({'message': 'Quantidade de recursos disponíveis inválida'}), 400
```


Esta parte verifica se já existe uma reserva para a mesma sala na data e horário especificados. Se existir, uma mensagem de erro é retornada.
```python
        with banco.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM reservas WHERE sala_id = %s AND data_inicio = %s", (sala_id, data_inicio))
            if cursor.fetchone():
                return jsonify({'message': 'Já existe uma reserva para esta sala nesta data e horário'}), 400
```

Aqui é verificado se a data de início da reserva é no futuro em relação à data atual. Se não for, uma mensagem de erro é retornada.
```python       
        data_atual = datetime.now().strftime('%Y-%m-%dT%H:%M')
        if data_inicio < data_atual:
            return jsonify({'message': 'A data de início da reserva deve ser no futuro'}), 400
```



Parte que verifica se o usuário que está fazendo a reserva existe no banco de dados. Se não existir, uma mensagem de erro é retornada.
```python  
        with banco.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM acesso WHERE user = %s", (usuario,))
            if not cursor.fetchone():
                return jsonify({'message': 'Usuário não encontrado'}), 400
```

Verificar se já existe uma reserva para a mesma sala, data e horário.
```python 
            cursor.execute("SELECT * FROM reservas WHERE sala_id = %s AND data_inicio = %s", (sala_id, data_inicio))
            if cursor.fetchone():
                return jsonify({'message': 'Já existe uma reserva para esta sala nesta data e horário'}), 400
```

Se todas as verificações passarem, a reserva é inserida no banco de dados e uma mensagem de sucesso é formatada e retornada para o usuário, confirmando a reserva.
```python 
        with banco.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO reservas (id, sala_id, data_inicio, duracao, usuario) VALUES (%s, %s, %s, %s, %s)", (id_reserva, sala_id, data_inicio, duracao, usuario))
            mydb.commit()

        data_formatada = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M').strftime('%d de %B de %Y')
        mensagem = f"Parabéns, sua reserva foi realizada. Não esqueça que foi para o dia {data_formatada} e por apenas {duracao} horas."

        return mensagem
```

Se a solicitação for do tipo GET, ou seja, o usuário está acessando a página de reserva, recuperamos as salas disponíveis do banco de dados e renderizamos a página reserva.html, passando as salas e a quantidade de recursos disponíveis como contexto para o template.
```python    
    with banco.conectaBanco() as mydb:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM salas")
        salas = [sala[1] for sala in cursor.fetchall()]  # Apenas os nomes das salas


    return render_template('reserva.html', salas=salas, projetores_disponiveis=projetores_disponiveis, caixas_som_disponiveis=caixas_som_disponiveis)
```

### Função minhas_reservas
Responsável por exibir as reservas feitas pelo usuário. Primeiramente, é verificado se o usuário está logado. Se não estiver, ele é redirecionado para a página de login. Em seguida, é obtido o nome do usuário logado da sessão. Após isso, as reservas associadas ao usuário logado do banco de dados são obtidas usando a função obterReservasUsuario do módulo banco (presente no arquivo `conf_banco.py`). Esta função retorna as reservas do usuário especificado.

Se nenhuma reserva for encontrada para o usuário, é exibido uma mensagem no terminal e o template minhas_reservas.html é rendenrizado, passando uma lista vazia de reservas. Se as reservas foram encontradas, o template `minhas_reservas.html` é renderizado, passando as reservas recuperadas como contexto. Este template é responsável por exibir as reservas na interface do usuário.
```python
@app.route('/minhas-reservas')
def minhas_reservas():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
o
    usuario = session['usuario_logado']

    # Exibir o nome do usuário logado no terminal (apenas para debug)
    print("Usuário logado:", usuario)

    reservas = banco.obterReservasUsuario(usuario)

    # Exibir as reservas do usuário logado no terminal (apenas para debug)
    print("Reservas do usuário:", reservas)

    if reservas is None:
        print("Nenhuma reserva encontrada para o usuário:", usuario)
        return render_template('minhas_reservas.html', reservas=[])

    return render_template('minhas_reservas.html', reservas=reservas)

```

### Função cancelar_reserva_formulario
Essa função recebe uma solicitação POST contendo o ID da reserva a ser cancelada. Primeiro, verifica se o usuário está logado. Em seguida, remove a reserva do banco de dados usando o ID fornecido. Se ocorrer algum erro durante o processo, uma mensagem de erro é retornada com o status 500. Caso contrário, uma mensagem de sucesso é retornada.
```python
@app.route('/cancelar-reserva', methods=['POST'])
def cancelar_reserva_formulario():
    # Verificar se o usuário está logado
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return jsonify({'message': 'Usuário não está logado'}), 401
   
    # Obter o ID da reserva a ser cancelada do formulário
    reserva_id = request.form['reserva_id']
   
    # Remover a reserva do banco de dados
    try:
        with banco.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
            mydb.commit()
    except Exception as e:
        # Em caso de erro, retornar uma mensagem de erro com status 500
        return jsonify({'message': f'Erro ao cancelar reserva: {e}'}), 500

    # Retornar uma mensagem de sucesso após cancelar a reserva
    return jsonify({'message': 'Reserva cancelada com sucesso'})
```

### Função logout
Responsável por encerrar a sessão do usuário e redirecioná-lo para a página inicial (página de login). Ela define o usuário logado como None, o que efetivamente encerra a sessão do usuário. Em seguida, redireciona o usuário para a página inicial (index), que é a página de login.
```python
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Definir o usuário logado como None para encerrar a sessão
    session['usuario_logado'] = None
    # Redirecionar para a página inicial (página de login)
    return redirect(url_for('index'))
```