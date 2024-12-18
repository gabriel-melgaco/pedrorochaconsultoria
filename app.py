from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from peewee import *
from datetime import datetime
from flask_mail import Mail, Message
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os



db = SqliteDatabase('dados.db')
load_dotenv()
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False  # Deve ser False para o port 465
app.config['MAIL_USE_SSL'] = True   # Deve ser True para o port 465

#CONFIGURAR VIRTUAL ENV QUANDO FOR HOSPEDAR NA WEB
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_TOKEN')
app.config['DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD')

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


mail = Mail(app)

class Clientes(Model):
    nome = CharField()
    email = CharField()
    telefone = CharField()
    data = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.

db.connect()
db.create_tables([Clientes])

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/database")
def database():
    return render_template('database.html')

@app.route("/register", methods=['POST'])
def registrar():
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    data = datetime.now()


    # Registrar no banco de dados
    Clientes.create(nome=nome, email=email, telefone=telefone, data=data)
    clientes = Clientes.select()
    lista_clientes = []

    for cliente in clientes: #Cria um dicionário pra armazenar os dados
        lista_clientes.append({
            'Nome':cliente.nome,
            'Email':cliente.email,
            'Telefone':cliente.telefone,
            'Data':cliente.data
        })


    df = pd.DataFrame(lista_clientes) #converter a lista em um data framd
    output = BytesIO()#Cria um objeto em memória simulando um arquivo para escrever os dados
    writer = pd.ExcelWriter(output, engine='openpyxl')#escreve dados no formato excel no buffer de memória
    df.to_excel(writer, index=False, sheet_name='clientes')#transforma DataFrame do Pandas em uma planiha excel
    writer.close() #finalliza a escrita do arquivo Excel no buffer de memória
    output.seek(0) #reposiciona o ponteiro no inicio do buffer


    # Criar mensagem de e-mail
    mail_message = Message(
        subject="Confirmação de Registro",
        sender=app.config['MAIL_USERNAME'],  # Utilize a configuração do seu aplicativo
        recipients=['pedrorochabconsultoria@gmail.com'],  # Enviar e-mail
        body=f"""
            Confirmação de Registro
            O usuário, {nome}, acabou de se registrar em seu site!
            Recebemos seu telefone:{telefone} e e-mail: {email}.
            
            
            Seu banco de dados de clientes está em anexo.
    """
    )

    mail_message.attach(
        "clientes.xlsx",  # Nome do arquivo
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # Tipo MIME do Excel
        output.read()  # Conteúdo do arquivo
    )

    # Enviar e-mail
    mail.send(mail_message)

    # Redirecionar após o registro
    return redirect(f'https://calendly.com/pedrorochabconsultoria/consultoriaexpress')


@app.route("/download_database", methods=['POST'])
def download_database():
    data = request.get_json()
    password = data.get('password')
    print(password)

    if password == app.config.get('DATABASE_PASSWORD'):
        filename = 'dados.db'
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return jsonify({'status': 'error', 'message': 'Senha incorreta ou arquivo não encontrado!'}), 403


if __name__ == '__main__':
    app.run(debug=True)

