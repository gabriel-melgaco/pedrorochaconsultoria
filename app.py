from flask import Flask, render_template, request, redirect
from peewee import *
from datetime import datetime
from flask_mail import Mail, Message


db = SqliteDatabase('dados.db')


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False  # Deve ser False para o port 465
app.config['MAIL_USE_SSL'] = True   # Deve ser True para o port 465
app.config['MAIL_USERNAME'] = 'megdev99@gmail.com'
app.config['MAIL_PASSWORD'] = '@13985261776Gm'
app.config['MAIL_PASSWORD'] = 'lnxi sbiv dnrp hyym'


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

@app.route("/register", methods=['POST'])
def registrar():
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    data = datetime.now()
    ano = data.year
    mes = data.month

    # Registrar no banco de dados
    Clientes.create(nome=nome, email=email, telefone=telefone, data=data)
    clientes = Clientes.select()
    lista_clientes = []

    for cliente in clientes:
        cliente_info = f'Nome:{cliente.nome}, {cliente.email}, {cliente.telefone} às {cliente.data}'
        lista_clientes.append(cliente_info)

    # Criar mensagem de e-mail
    mail_message = Message(
        subject="Confirmação de Registro",
        sender=app.config['MAIL_USERNAME'],  # Utilize a configuração do seu aplicativo
        recipients=[email],  # Enviar e-mail para o usuário que preencheu o formulário
        body=f"""
            Confirmação de Registro
            O usuário, {nome}, acabou de se registrar em seu site!
            Recebemos seu telefone:{telefone} e e-mail: {email}.
            
            
            Seu banco de dados de cliente é:
            {lista_clientes}
    """
    )

    # Enviar e-mail
    mail.send(mail_message)

    # Redirecionar após o registro
    return redirect(f'https://calendly.com/pedrorochabconsultoria/30min?month={ano}-{mes}')

if __name__ == '__main__':
    app.run(debug=True)

