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
    
@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBanco()
    user = session.query(Pessoas).filter_by(usuario=usuario, senha=senha).all()
    if len(usuario) == 0:
        return {'status': 'usuario inexistente'}
    
    while True:
        token = token_hex(50)
        tokenExiste = session.query(Tokens).filter_by(token=Tokens).all()
        if len(tokenExiste) == 0:
            pessoaExiste = session.query(Tokens).filter_by(id_pessoa=user[0].id).all()
            if len(pessoaExiste) == 0:
                novoToken = Tokens(id_pessoa=user[0].id, token=token)
                session.add(novoToken)
                session.commit()
                
            break