from conf_banco import Banco
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import os
from datetime import datetime
import locale


app = Flask(__name__)
app.secret_key = 'k4mi'
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

banco = Banco() 


MAX_PROJETORES = 5
MAX_CAIXAS_SOM = 3
projetores_disponiveis = MAX_PROJETORES
caixas_som_disponiveis = MAX_CAIXAS_SOM


@app.route('/')
def index():
   return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       usuario = request.form['username']
       senha = request.form['password']
       user = banco.verificaUser(usuario) 
     
       if user and senha == user[2]:
           session['usuario_logado'] = user[3]
           return redirect(url_for('home', success_message='Login bem-sucedido!'))
       else:
           error = 'Usuario ou senha incorretos, tente novamente.'
           return render_template('index.html', error=error)
   return render_template('index.html')


@app.route('/home')
def home():
   if 'usuario_logado' not in session or session['usuario_logado'] is None:
       return redirect(url_for('login'))
   else:
       nome = session['usuario_logado']
  
       with banco.conectaBanco() as mydb:
           cursor = mydb.cursor()
           cursor.execute("SELECT * FROM salas")
           salas = [sala[1] for sala in cursor.fetchall()]  #Apenas os nomes das salas

       success_message = request.args.get('success_message')
       return render_template('pagina.html', nome=nome, salas=salas, success_message=success_message)


 
def listar_salas():
   salas = banco.obterSalas()
   return jsonify(salas)


@app.route('/reserva', methods=['GET', 'POST'])
def reserva():

   global projetores_disponiveis, caixas_som_disponiveis
 
   if 'usuario_logado' not in session or session['usuario_logado'] is None:
       return jsonify({'message': 'Usuário não está logado'}), 401

   if request.method == 'POST':
       sala_nome = request.form['sala']  # Nome da sala selecionada
       sala_id = banco.obterSalaPorNome(sala_nome)  # ID da sala selecionada
       sala_id = request.form['sala']
       data_inicio = request.form['data_inicio']
       duracao = request.form['duracao']
       usuario = request.form['usuario']
       projetor = request.form.get('projetor') 
       caixa_som = request.form.get('caixa_som')

     
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
     

       #declarações para que todas as reservas não tenham id=0
       id_reserva = None

       sala_id = banco.obterSalaPorNome(sala_nome)  
       if sala_id is None:
           return jsonify({'message': 'Sala não encontrada'}), 400
       

       # Verificar se já existe uma reserva para a mesma sala, data e horário
       with banco.conectaBanco() as mydb:
           cursor = mydb.cursor()
           cursor.execute("SELECT * FROM reservas WHERE sala_id = %s AND data_inicio = %s", (sala_id, data_inicio))
           if cursor.fetchone():
               return jsonify({'message': 'Já existe uma reserva para esta sala nesta data e horário'}), 400
     
       #Verificação da data de início da reserva e do usuário
       data_atual = datetime.now().strftime('%Y-%m-%dT%H:%M')
       if data_inicio < data_atual:
           return jsonify({'message': 'A data de início da reserva deve ser no futuro'}), 400


       with banco.conectaBanco() as mydb:
           cursor = mydb.cursor()
           cursor.execute("SELECT * FROM acesso WHERE user = %s", (usuario,))
           if not cursor.fetchone():
               return jsonify({'message': 'Usuário não encontrado'}), 400


           # verificar se já existe uma reserva para a mesma sala, data e horário
           cursor.execute("SELECT * FROM reservas WHERE sala_id = %s AND data_inicio = %s", (sala_id, data_inicio))
           if cursor.fetchone():
               return jsonify({'message': 'Já existe uma reserva para esta sala nesta data e horário'}), 400



        #Inserção das reservas no banco de dados
       with banco.conectaBanco() as mydb:
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO reservas (id, sala_id, data_inicio, duracao, usuario) VALUES (%s, %s, %s, %s, %s)", (id_reserva, sala_id, data_inicio, duracao, usuario))
            mydb.commit()


            data_formatada = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M').strftime('%d de %B de %Y')
            mensagem = f"Parabéns, sua reserva foi realizada. Não esqueça que foi para o dia {data_formatada} e por apenas {duracao} horas."

       return mensagem
 

   with banco.conectaBanco() as mydb:
       cursor = mydb.cursor()
       cursor.execute("SELECT * FROM salas")
       salas = [sala[1] for sala in cursor.fetchall()]  # Apenas os nomes das salas


   return render_template('reserva.html', salas=salas, projetores_disponiveis=projetores_disponiveis, caixas_som_disponiveis=caixas_som_disponiveis)



@app.route('/minhas-reservas')
def minhas_reservas():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))


    usuario = session['usuario_logado']


    # Verificando se os dados do usuário estão corretos
    print("Usuário logado:", usuario)


    # Obter as reservas do usuário logado
    reservas = banco.obterReservasUsuario(usuario)


    # Verificando se as reservas foram recuperadas corretamente do banco de dados
    print("Reservas do usuário:", reservas)


    if reservas is None:
       print("Nenhuma reserva encontrada para o usuário:", usuario)
       return render_template('minhas_reservas.html', reservas=[])


    return render_template('minhas_reservas.html', reservas=reservas)




@app.route('/cancelar-reserva', methods=['POST'])
def cancelar_reserva_formulario():
   if 'usuario_logado' not in session or session['usuario_logado'] is None:
       return jsonify({'message': 'Usuário não está logado'}), 401
 
   reserva_id = request.form['reserva_id']
 
   # Remover a reserva do banco de dados
   try:
       with banco.conectaBanco() as mydb:
           cursor = mydb.cursor()
           cursor.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
           mydb.commit()
   except Exception as e:
       return jsonify({'message': f'Erro ao cancelar reserva: {e}'}), 500

   return jsonify({'message': 'Reserva cancelada com sucesso'})

 
@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session['usuario_logado'] = None
   return redirect(url_for('index'))


# RODA A APLICAÇAO
if __name__ == '__main__':
   app.run(debug=True)