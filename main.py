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
            return redirect(url_for('home'))
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

        return render_template('pagina.html', nome=nome, salas=salas)

    
def listar_salas():
    salas = banco.obterSalas()
    return jsonify(salas)

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return jsonify({'message': 'Usuário não está logado'}), 401

    if request.method == 'POST':
        sala_id = request.form['sala']
        data_inicio = request.form['data_inicio']
        duracao = request.form['duracao']
        usuario = request.form['usuario']
        
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

            
            cursor.execute("INSERT INTO reservas (sala_id, data_inicio, duracao, usuario) VALUES (%s, %s, %s, %s)", (sala_id, data_inicio, duracao, usuario))
            mydb.commit()

        
        data_formatada = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M').strftime('%d de %B de %Y')
        mensagem = f"Parabéns, sua reserva foi realizada. Não esqueça que foi para o dia {data_formatada} e por apenas {duracao} horas."

        return mensagem

    return render_template('reserva.html')






@app.route('/cancelar-reserva', methods=['POST'])
def cancelar_reserva():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return jsonify({'message': 'Usuário não está logado'}), 401
    
    reserva_id = request.form['reserva_id'] 
    
    with banco.conectaBanco() as mydb:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
        mydb.commit()

    return jsonify({'message': 'Reserva cancelada com sucesso'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    return redirect(url_for('index'))


# RODA A APLICAÇAO 
if __name__ == '__main__':
    app.run(debug=True)
