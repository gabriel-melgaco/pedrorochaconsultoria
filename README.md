# BIO Pessoal: Flask App com Registro de Clientes e Envio de E-mail

Este projeto é uma aplicação Flask que permite registrar clientes em um banco de dados SQLite, gerar uma planilha Excel com as informações registradas, e enviar essa planilha por e-mail automaticamente para um destinatário específico. O envio do e-mail é feito utilizando o Flask-Mail, e as informações de configuração (como login e senha) são gerenciadas por variáveis de ambiente.

## Funcionalidades

- Registro de clientes com nome, e-mail e telefone.
- Armazenamento dos dados dos clientes no banco de dados SQLite.
- Geração de um arquivo Excel contendo todos os clientes registrados.
- Envio automático de um e-mail com o arquivo Excel em anexo.
- Redirecionamento para uma página de consultoria e agendamento de videoconferências após o registro.

## Tecnologias Utilizadas

- **Flask**: Framework web utilizado para criar as rotas e o servidor da aplicação.
- **Peewee**: ORM (Object Relational Mapping) usado para modelar o banco de dados SQLite.
- **Flask-Mail**: Extensão Flask para o envio de e-mails.
- **Pandas**: Utilizado para converter os dados do banco de dados em um DataFrame e gerar o arquivo Excel.
- **Openpyxl**: Biblioteca usada pelo Pandas para criar o arquivo Excel.
- **SQLite**: Banco de dados utilizado para armazenar os dados dos clientes.
- **dotenv**: Gerenciamento de variáveis de ambiente para manter as credenciais seguras.

## Pré-requisitos

Para rodar o projeto localmente, você precisa ter instalado:

- Python 3.x
- Um servidor de e-mail configurado (Gmail no exemplo abaixo)
- O arquivo `.env` com as credenciais do servidor de e-mail

## Configuração do Ambiente

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
