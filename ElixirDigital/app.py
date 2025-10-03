import mysql.connector
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'elixir_digital_secret_key_2025'

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "carmen",
    "port": 3306,
    "database": "ElixirDigital",
    "autocommit": True
}

# Função para obter conexão com tratamento de erro
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar com o MySQL: {err}")
        return None

# Testar conexão ao iniciar
def test_connection():
    max_retries = 3
    for i in range(max_retries):
        connection = get_db_connection()
        if connection:
            print("✅ Conexão com o MySQL estabelecida com sucesso!")
            connection.close()
            return True
        else:
            print(f"❌ Tentativa {i+1}/{max_retries} falhou. Tentando novamente...")
            time.sleep(2)
    
    print("❌ Não foi possível estabelecer conexão com o MySQL após várias tentativas")
    return False

# Testar conexão ao iniciar a aplicação
test_connection()

# Função para buscar feedbacks do banco
def get_feedbacks_from_db(limit=None):
    connection = get_db_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT autor, mensagem, avaliacao, dt 
            FROM feedback 
            WHERE origem_cliente = TRUE 
            ORDER BY dt DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        feedbacks = cursor.fetchall()
        
        # Formatar os dados
        formatted_feedbacks = []
        for feedback in feedbacks:
            # Converter avaliação para estrelas
            rating = feedback['avaliacao'] or 0
            stars_html = ''
            for i in range(1, 6):
                if i <= rating:
                    stars_html += '<i class="fas fa-star"></i>'
                else:
                    stars_html += '<i class="far fa-star"></i>'
            
            formatted_feedbacks.append({
                'autor': feedback['autor'],
                'mensagem': feedback['mensagem'],
                'avaliacao': stars_html,
                'data': feedback['dt'].strftime('%d/%m/%Y') if feedback['dt'] else 'Data não informada'
            })
        
        return formatted_feedbacks
        
    except mysql.connector.Error as err:
        print(f"Erro ao buscar feedbacks: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

# Função para verificar se o admin está logado
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route("/")
def index():
    team = [
    {
        "nome": "Anna Rodrigues",
        "foto": "img/alunos/Cropadas/Anna (Edited).jpeg",
        "especialidade": "",
        "descricao": "Anna Julia Rodrigues, 17 anos. com interesse em me especializar em Banco de dados. No projeto atuei no grupo de desenvolvimento Banco de dados.",
        "linkedin": "https://www.linkedin.com/in/anna-j%C3%BAlia-rodrigues-22a298274/",
        "github": "https://github.com/Annaju061"
    },
    {
        "nome": "Cauã Rodrigo",
        "foto": "img/alunos/Cropadas/Caua Rodrigues (Edited).jpeg",
        "especialidade": "",
        "descricao": "Cauã Rodrigo, 16 anos. com interesse em me especializar em Banco de Dados. No projeto atuei no grupo de desenvolvimento Back-End.",
        "linkedin": "https://www.linkedin.com/in/cau%C3%A3-rodrigo-a42147304",
        "github": "https://github.com/cauarodri7"
    },
    {
        "nome": "Cauã Silva",
        "foto": "img/alunos/Cropadas/Caua Silva (Edited).jpeg",
        "especialidade": "",
        "descricao": "Cauã da Silva, 16 anos. com interesse em me especializar em full-Stack. No projeto atuei no grupo de desenvolvimento banco de Dados.",
        "linkedin": "https://www.linkedin.com/in/cau%C3%A3-da-silva-carvalho-a2026a313/",
        "github": "https://github.com/MeboxT3R1A"
    },
    {
        "nome": "Davi Marcelo",
        "foto": "img/alunos/Cropadas/Davi (Edited).jpeg",
        "especialidade": "",
        "descricao": "Davi Marcelo, 16 anos. com interesse em me especializar em Back-End. No projeto atuei no grupo de desenvolvimento Back-End.",
        "linkedin": "https://www.linkedin.com/in/davi-silva-55653a321",
        "github": "https://github.com/DaviMarcelo"
    },
    {
        "nome": "Érick Matheus",
        "foto": "img/alunos/Cropadas/Erick (Edited).jpeg",
        "especialidade": "",
        "descricao": "Erick Matheus, 16 anos. com interesse em me especializar em Análise e Requisitos No projeto atuei no grupo de desenvolvimento Requisitos.",
        "linkedin": "https://br.linkedin.com/in/erick-matheus-374382387",
        "github": "#"
    },
    {
        "nome": "Gabriel Gomes",
        "foto": "img/alunos/Cropadas/Gabriel Gomes (Edited).jpeg",
        "especialidade": "",
        "descricao": "Gabriel Gomes, 18 anos. com interesse em me especializar em banco de dados. No projeto atuei no grupo de desenvolvimento back-End.",
        "linkedin": "https://www.linkedin.com/in/gabriel-gomes-207848357",
        "github": "https://github.com/GAVIMINI"
    },
    {
        "nome": "Gabriel Pereira",
        "foto": "img/alunos/Cropadas/Gabriel Lopes (Edited).jpeg",
        "especialidade": "",
        "descricao": "Gabriel Pereira, 18 anos. com interesse em me especializar em Full-Stack. No projeto atuei no grupo de desenvolvimento Banco de Dados.",
        "linkedin": "https://www.linkedin.com/in/gabriel-pereira-9a6a3a357/",
        "github": "https://github.com/LopesGP1"
    },
    {
        "nome": "Jhone Alves",
        "foto": "img/alunos/Cropadas/Jhone (Edited).jpeg",
        "especialidade": "",
        "descricao": "Jhone Alves, 17 anos. com interesse em me especializar em Front-End. No projeto atuei no grupo de desenvolvimento Front-End.",
        "linkedin": "https://www.linkedin.com/in/jhone-alves-2ba91b182/",
        "github": "https://github.com/eclipsepackage"
    },
    {
        "nome": "João Cruz",
        "foto": "img/alunos/Cropadas/joao Pedro (Edited).jpeg",
        "especialidade": "",
        "descricao": "João Cruz, 17 anos. com interesse em me especializar em Análise e Requisitos No projeto atuei no grupo de desenvolvimento Requisitos.",
        "linkedin": "https://www.linkedin.com/in/jo%C3%A3o-pedro-cruz-2a1a5a357/",
        "github": "https://github.com/japaNBA"
    },
    {
        "nome": "Jonatas Torres",
        "foto": "img/alunos/Cropadas/Jonatas (Edited).jpeg",
        "especialidade": "",
        "descricao": "Jonatas Torres, 16 anos. com interesse em me especializar em Full-Stack. No projeto atuei no grupo de desenvolvimento Front-End.",
        "linkedin": "https://www.linkedin.com/in/jonatas-torres-73ab42308",
        "github": "https://github.com/Jota-bsb"
    },
    {
        "nome": "Kaique Alves",
        "foto": "img/alunos/Cropadas/Kaique (Edited).jpeg",
        "especialidade": "",
        "descricao": "Kaique Alves, 18 anos. com interesse em me especializar em Gestão de TI. No projeto atuei no grupo de desenvolvimento Banco de Dados.",
        "linkedin": "https://www.linkedin.com/in/kaique-alves-de-sousa-alves-de-sousa-a62487363?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app",
        "github": "https://github.com/kaiqueAlves-s"
    },
    {
        "nome": "Luana Agnes",
        "foto": "img/alunos/Cropadas/Luana (Edited).jpeg",
        "especialidade": "",
        "descricao": "Luana Agnes, 16 anos. com interesse em me especializar em Back-End e Banco de Dados. No projeto atuei no grupo de desenvolvimento front-end.",
        "linkedin": "linkedin.com/in/l-a-bellini-b94569387",
        "github": "#"
    },
    {
        "nome": "Pâmella Freitas",
        "foto": "img/alunos/Cropadas/Pamella (Edited).jpeg",
        "especialidade": "",
        "descricao": "Pâmella Freitas, 16 anos. com interesse em me especializar em Gestão de TI. No projeto atuei como Scrum Master.",
        "linkedin": "https://br.linkedin.com/in/p%C3%A2mella-figueira-83644a2ba",
        "github": "https://github.com/pamellaff"
    },
    {
        "nome": "Pedro William",
        "foto": "img/alunos/Cropadas/Pedro (Edited).jpeg",
        "especialidade": "",
        "descricao": "Pedro William, 17 anos. com interesse em me especializar em Banco de Dados. No projeto atuei no grupo de desenvolvimento Back-end.",
        "linkedin": "https://www.linkedin.com/in/pedro-cassimiro",
        "github": "https://github.com/pedrowilliam7502-sketch"
    },
    {
        "nome": "Riquelme Almeida",
        "foto": "img/alunos/Cropadas/Riquelme (Edited).jpeg",
        "especialidade": "",
        "descricao": "Riquelme Almeida, 16 anos. com interesse em me especializar em Análise e Requisitos . No projeto atuei no grupo de desenvolvimento Requisitos.",
        "linkedin": "https://www.linkedin.com/in/riquelme-silva-058b54387",
        "github": "#"
    },
    {
        "nome": "Ryan Souza",
        "foto": "img/alunos/Cropadas/Ryan (Edited).jpeg",
        "especialidade": "",
        "descricao": "Ryan Souza, 16 anos. com interesse em me especializar em Banco de Dados. No projeto atuei no grupo de desenvolvimento Front-end.",
        "linkedin": "https://www.linkedin.com/in/ryan-lucas-532a26387/",
        "github": "https://github.com/ryanlucas54189-alt"
    },
    {
        "nome": "Vinícius Aquino",
        "foto": "img/alunos/Cropadas/Vinicius (Edited).jpeg",
        "especialidade": "",
        "descricao": "Vinicius Aquino, 17 anos. com interesse em me especializar em Front-end No projeto atuei no grupo de desenvolvimento Requisitos.",
        "linkedin": "https://www.linkedin.com/in/vinicius-aquino-973512308",
        "github": "https://github.com/vinicius-a08"
    },
    {
        "nome": "Vitor Hugo",
        "foto": "img/alunos/Cropadas/Vitor (Edited).jpeg",
        "especialidade": "",
        "descricao": "Vitor Hugo, 18 anos. com interesse em me especializar em Programação para jogos. No projeto atuei no grupo de desenvolvimento Requisitos.",
        "linkedin": "#",
        "github": "#"
    }
    ]
    
    # Buscar feedbacks para a página inicial (limite de 3 para o carrossel)
    feedbacks = get_feedbacks_from_db(limit=3)
    
    return render_template("index.html", team=team, feedbacks=feedbacks)

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/feedback")
def feedback():
    # Buscar todos os feedbacks para a página de feedback
    feedbacks = get_feedbacks_from_db()
    return render_template("feedback.html", feedbacks=feedbacks)

@app.route("/salvar_feedback", methods=["POST"])
def salvar_feedback():
    nome = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    project = request.form.get("project", "").strip() or None
    rating = request.form.get("rating", "").strip()
    message = request.form.get("message", "").strip()

    if not nome or not email or not rating or not message:
        return "Preencha todos os campos obrigatórios.", 400

    try:
        avaliacao = int(rating)
    except ValueError:
        avaliacao = None

    connection = get_db_connection()
    if not connection:
        return "Erro de conexão com o banco de dados.", 500

    cursor = connection.cursor()
    try:
        sql_feedback = """
            INSERT INTO feedback (mensagem, autor, email, projeto, avaliacao, origem_cliente)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores_feedback = (message, nome, email, project, avaliacao, True)
        cursor.execute(sql_feedback, valores_feedback)
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        return f"Erro ao salvar no banco: {err}", 500
    finally:
        cursor.close()
        connection.close()

    # Buscar feedbacks atualizados após salvar
    feedbacks = get_feedbacks_from_db()
    return render_template("feedback.html", sucesso=True, feedbacks=feedbacks)

@app.route("/forms")
def forms():
    return render_template("forms.html")

@app.route("/forms_solicitacao", methods=["POST"])
def forms_solicitacao():
    company = request.form.get("company", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    technologies = request.form.get("technologies", "").strip() or None
    description = request.form.get("description", "").strip()

    if not company or not email or not phone or not description:
        return "Por favor preencha todos os campos obrigatórios.", 400

    connection = get_db_connection()
    if not connection:
        return "Erro de conexão com o banco de dados.", 500

    cursor = connection.cursor(buffered=True)
    try:
        connection.start_transaction()

        cursor.execute("SELECT id_cliente FROM cliente WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            cliente_id = row[0]
            cursor.execute(
                "UPDATE cliente SET nome = %s, telefone = %s WHERE id_cliente = %s",
                (company, phone, cliente_id)
            )
        else:
            cursor.execute(
                "INSERT INTO cliente (nome, email, telefone) VALUES (%s, %s, %s)",
                (company, email, phone)
            )
            cliente_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO pedido (descricao, status, tecnologias_preferidas, fk_cliente)
            VALUES (%s, %s, %s, %s)
            """,
            (description, "Em análise", technologies, cliente_id)
        )
        pedido_id = cursor.lastrowid

        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        print("Erro DB /forms_solicitacao:", err)
        return f"Erro ao salvar solicitação: {err}", 500
    finally:
        cursor.close()
        connection.close()

    return render_template("forms.html", sucesso=True, pedido_id=pedido_id)

@app.route("/login")
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    return render_template("login.html")

@app.route("/admin/login", methods=["POST"])
def admin_login():
    try:
        data = request.get_json()
        print(f"Dados recebidos: {data}")
        
        if not data:
            return jsonify({'success': False, 'message': 'Dados não recebidos'}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        print(f"Tentando login com usuário: '{username}' e senha: '{password}'")
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Usuário e senha são obrigatórios'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Erro de conexão com o banco de dados'}), 500
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id_administrador, nome, email, senha FROM administrador WHERE email = %s",
                (username,)
            )
            admin = cursor.fetchone()
            
            if admin:
                print(f"Administrador encontrado: {admin['email']}")
                print(f"Senha no banco: {admin['senha']}")
                print(f"Senha fornecida: {password}")
                
                # Verificar senha diretamente (sem hash)
                if password == admin['senha']:
                    session['admin_logged_in'] = True
                    session['admin_id'] = admin['id_administrador']
                    session['admin_name'] = admin['nome']
                    print("Login bem-sucedido!")
                    return jsonify({
                        'success': True, 
                        'message': f'Login realizado com sucesso. Bem-vindo, {admin["nome"]}!'
                    })
                else:
                    print("Senha incorreta")
                    return jsonify({'success': False, 'message': 'Senha incorreta'}), 401
            else:
                print("Administrador não encontrado")
                return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 401
                
        except mysql.connector.Error as err:
            print(f"Erro no banco de dados: {err}")
            return jsonify({'success': False, 'message': 'Erro no servidor'}), 500
        finally:
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'}), 500

@app.route("/admin")
@admin_required
def admin():
    connection = get_db_connection()
    if not connection:
        return "Erro de conexão com o banco de dados.", 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id_pedido, p.descricao, p.dt, p.status, p.tecnologias_preferidas,
                   c.nome as company, c.email, c.telefone as phone
            FROM pedido p
            JOIN cliente c ON p.fk_cliente = c.id_cliente
            ORDER BY p.dt DESC
        """)
        pedidos = cursor.fetchall()
        
        # Formatar os dados para o template
        requests_data = []
        for pedido in pedidos:
            # Mapear status para exibição
            status_display = {
                'Em análise': 'Em Análise',
                'Em produção': 'Em Produção', 
                'Finalizando': 'Finalizando',
                'Não aceito': 'Não Aceito'
            }
            
            requests_data.append({
                'id': pedido['id_pedido'],
                'company': pedido['company'],
                'email': pedido['email'],
                'phone': pedido['phone'],
                'description': pedido['descricao'],
                'technologies': pedido['tecnologias_preferidas'].split(', ') if pedido['tecnologias_preferidas'] else [],
                'status': pedido['status'].lower().replace(' ', '_').replace('ç', 'c'),
                'status_display': status_display.get(pedido['status'], pedido['status']),
                'created_at': pedido['dt'].strftime('%Y-%m-%d %H:%M:%S') if pedido['dt'] else None,
                'formatted_date': pedido['dt'].strftime('%d/%m/%Y') if pedido['dt'] else 'Data não informada'
            })
        
        # Calcular estatísticas
        total = len(pedidos)
        in_production = len([p for p in pedidos if p['status'] == 'Em produção'])
        completed = len([p for p in pedidos if p['status'] == 'Finalizando'])
        rejected = len([p for p in pedidos if p['status'] == 'Não aceito'])
        
    except mysql.connector.Error as err:
        print("Erro ao buscar pedidos:", err)
        requests_data = []
        total = in_production = completed = rejected = 0
    finally:
        cursor.close()
        connection.close()
    
    return render_template("admin.html", 
                         requests=requests_data,
                         total_requests=total,
                         in_production_requests=in_production,
                         completed_requests=completed,
                         rejected_requests=rejected)

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    return redirect(url_for('index'))

@app.route("/acompanhamento")
def acompanhamento():
    return render_template("acompanhamento.html")

# API para buscar pedidos por email
@app.route("/api/acompanhamento", methods=["POST"])
def api_acompanhamento():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'success': False, 'message': 'Email é obrigatório'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Erro de conexão com o banco de dados'}), 500
    
    cursor = connection.cursor(dictionary=True)
    try:
        # Buscar pedidos do cliente pelo email
        cursor.execute("""
            SELECT p.id_pedido, p.descricao, p.dt, p.status, p.tecnologias_preferidas,
                   c.nome as company, c.email, c.telefone as phone
            FROM pedido p
            JOIN cliente c ON p.fk_cliente = c.id_cliente
            WHERE c.email = %s
            ORDER BY p.dt DESC
        """, (email,))
        
        pedidos = cursor.fetchall()
        
        if not pedidos:
            return jsonify({
                'success': False, 
                'message': 'Nenhuma solicitação encontrada para este email'
            }), 404
        
        # Formatar os dados para resposta
        requests_data = []
        for pedido in pedidos:
            # Mapear status para exibição
            status_display = {
                'Em análise': 'Em Análise',
                'Em produção': 'Em Produção', 
                'Finalizando': 'Finalizando',
                'Não aceito': 'Não Aceito'
            }
            
            # Mapear classes CSS para status
            status_class = {
                'Em análise': 'status-pending',
                'Em produção': 'status-approved',
                'Finalizando': 'status-approved',
                'Não aceito': 'status-rejected'
            }
            
            requests_data.append({
                'id': pedido['id_pedido'],
                'company': pedido['company'],
                'email': pedido['email'],
                'phone': pedido['phone'] or 'Não informado',
                'description': pedido['descricao'],
                'technologies': pedido['tecnologias_preferidas'] or 'Não especificadas',
                'status': pedido['status'],
                'status_display': status_display.get(pedido['status'], pedido['status']),
                'status_class': status_class.get(pedido['status'], 'status-pending'),
                'created_at': pedido['dt'].strftime('%Y-%m-%d %H:%M:%S') if pedido['dt'] else None,
                'formatted_date': pedido['dt'].strftime('%d/%m/%Y') if pedido['dt'] else 'Data não informada'
            })
        
        return jsonify({
            'success': True,
            'requests': requests_data
        })
        
    except mysql.connector.Error as err:
        print("Erro ao buscar pedidos:", err)
        return jsonify({
            'success': False, 
            'message': 'Erro interno do servidor'
        }), 500
    finally:
        cursor.close()
        connection.close()

@app.route("/teste_conexao")
def teste_conexao():
    connection = get_db_connection()
    if connection:
        connection.close()
        return "Conectado ao banco com sucesso!"
    else:
        return "Falha na conexão com o banco."

# API para atualizar status (para o JavaScript)
@app.route("/api/requests/<int:request_id>/status", methods=["PUT"])
@admin_required
def update_request_status(request_id):
    data = request.get_json()
    new_status = data.get('status')
    
    # Mapear status do JavaScript para status do banco
    status_map = {
        'in_production': 'Em produção',
        'completed': 'Finalizando', 
        'rejected': 'Não aceito'
    }
    
    db_status = status_map.get(new_status, 'Em análise')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Erro de conexão com o banco de dados'}), 500
    
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE pedido SET status = %s WHERE id_pedido = %s",
            (db_status, request_id)
        )
        connection.commit()
        return jsonify({'success': True, 'message': 'Status atualizado com sucesso'})
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'success': False, 'message': f'Erro ao atualizar status: {err}'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)