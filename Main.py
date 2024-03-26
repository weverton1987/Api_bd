from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Models import CONN, Pessoas, Tokens
from secrets import token_hex

app = FastAPI()

def conectaBanco():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/cadastro')
def cadastro(nome: str, user: str, senha: str):
    session = conectaBanco()
    usuario = session.query(Pessoas).filter_by(usuario=user, senha=senha).all()
    if len(usuario) == 0:
        x = Pessoas(nome= nome, usuario= user, senha= senha)
        session.add(x)
        session.commit()
        return {'status', 'Sucesso'}
    elif len(usuario) > 0:
        return {'status': 'Usuário já cadastrado.'}