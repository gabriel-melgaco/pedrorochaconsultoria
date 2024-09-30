from flask import Flask, render_template, request, redirect
from peewee import *
from datetime import datetime

db = SqliteDatabase('dados.db')


app = Flask(__name__)

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

    Clientes.create(nome=nome, email=email, telefone=telefone, data=data)
    return redirect(f'https://calendly.com/pedrorochabconsultoria/30min?month={ano}-{mes}')

if __name__ == '__main__':
    app.run(debug=True)

