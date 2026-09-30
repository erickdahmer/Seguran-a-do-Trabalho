import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta_ehs_jbdias_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELOS DO BANCO DE DADOS ====================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(50), default="TST")

class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nome = db.Column(db.String(100), nullable=False)
    funcao = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(50), default="JB DIAS")

class RegistroEHS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20))
    data = db.Column(db.String(10), nullable=False)
    programa = db.Column(db.String(50), nullable=False)
    empresa = db.Column(db.String(50), default="JB DIAS")
    responsavel = db.Column(db.String(100))
    lider = db.Column(db.String(100))
    colaborador_envolvido = db.Column(db.String(100))
    houve_desvio = db.Column(db.String(10))
    qtd_pessoas = db.Column(db.Integer, default=1)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(30), default="Concluído")

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'sucesso': False, 'mensagem': 'E-mail já cadastrado.'}), 400
    
    senha_hash = generate_password_hash(data['senha'])
    novo_usuario = Usuario(
        nome=data['nome'], 
        email=data['email'], 
        senha_hash=senha_hash, 
        cargo=data.get('cargo', 'TST')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'sucesso': True, 'mensagem': 'Usuário cadastrado com sucesso!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if usuario and check_password_hash(usuario.senha_hash, data['senha']):
        session['user_id'] = usuario.id
        session['user_nome'] = usuario.nome
        return jsonify({'sucesso': True, 'usuario': {'nome': usuario.nome, 'email': usuario.email}})
    
    return jsonify({'sucesso': False, 'mensagem': 'E-mail ou senha incorretos.'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'sucesso': True})

@app.route('/api/usuario-atual', methods=['GET'])
def usuario_atual():
    if 'user_id' in session:
        user = Usuario.query.get(session['user_id'])
        return jsonify({'logado': True, 'usuario': {'nome': user.nome, 'email': user.email}})
    return jsonify({'logado': False})

# ==================== ROTAS DE DADOS (CRUD) ====================

@app.route('/api/registros', methods=['GET', 'POST'])
def gerenciar_registros():
    if 'user_id' not in session:
        return jsonify({'mensagem': 'Não autorizado'}), 401
        
    if request.method == 'GET':
        registros = RegistroEHS.query.order_by(RegistroEHS.id.desc()).all()
        return jsonify([{
            'id_db': r.id,
            'id': r.codigo,
            'data': r.data,
            'programa': r.programa,
            'empresa': r.empresa,
            'responsavel': r.responsavel,
            'lider': r.lider,
            'colaborador_envolvido': r.colaborador_envolvido,
            'houve_desvio': r.houve_desvio,
            'qtd_pessoas': r.qtd_pessoas,
            'descricao': r.descricao,
            'status': r.status
        } for r in registros])
    
    if request.method == 'POST':
        data = request.json
        novo = RegistroEHS(
            codigo=f"REG-{RegistroEHS.query.count() + 1:03d}",
            data=data['data'],
            programa=data['programa'],
            empresa="JB DIAS",
            responsavel=data['responsavel'],
            lider=data['lider'],
            colaborador_envolvido=data['colaborador_envolvido'],
            houve_desvio=data['houve_desvio'],
            qtd_pessoas=data['qtd_pessoas'],
            descricao=data['descricao'],
            status="Concluído"
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'sucesso': True})

@app.route('/api/colaboradores', methods=['GET', 'POST'])
def gerenciar_colaboradores():
    if 'user_id' not in session:
        return jsonify({'mensagem': 'Não autorizado'}), 401

    if request.method == 'GET':
        colabs = Colaborador.query.all()
        return jsonify([{'id': c.codigo, 'nome': c.nome, 'funcao': c.funcao, 'empresa': c.empresa} for c in colabs])

    if request.method == 'POST':
        data = request.json
        novo = Colaborador(
            codigo=f"COL-{Colaborador.query.count() + 1:03d}",
            nome=data['nome'],
            funcao=data['funcao'],
            empresa="JB DIAS"
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'sucesso': True})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)