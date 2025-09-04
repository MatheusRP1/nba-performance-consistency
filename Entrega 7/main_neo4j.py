from fastapi import FastAPI, HTTPException
from typing import Optional
import crud_neo4j
from pydantic import BaseModel

app = FastAPI(title="NBA Neo4j API")

# ================== MODELOS ==================

class Jogador(BaseModel):
    nome: str
    posicao: str
    time_nome: str

class UpdateJogador(BaseModel):
    posicao: Optional[str] = None

class Time(BaseModel):
    nome: str
    cidade: str

class UpdateTime(BaseModel):
    cidade: Optional[str] = None

class Partida(BaseModel):
    id_partida: str
    time_casa: str
    time_fora: str
    data: str
    pontos_casa: int
    pontos_fora: int

class UpdatePartida(BaseModel):
    pontos_casa: Optional[int] = None
    pontos_fora: Optional[int] = None

# ================== ROTAS JOGADORES ==================

@app.post("/jogadores/")
def criar_jogador(jogador: Jogador):
    crud_neo4j.create_jogador(jogador.nome, jogador.posicao, jogador.time_nome)
    return {"mensagem": "Jogador criado com sucesso!"}

@app.get("/jogadores/")
def listar_jogadores():
    return crud_neo4j.read_jogadores()

@app.put("/jogadores/{nome}")
def atualizar_jogador(nome: str, dados: UpdateJogador):
    if not dados.posicao:
        raise HTTPException(status_code=400, detail="Nada para atualizar")
    result = crud_neo4j.update_jogador_posicao(nome, dados.posicao)
    if not result:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return {"atualizado": result}

@app.delete("/jogadores/{nome}")
def deletar_jogador(nome: str):
    crud_neo4j.delete_jogador(nome)
    return {"mensagem": f"Jogador {nome} removido"}

# ================== ROTAS TIMES ==================

@app.post("/times/")
def criar_time(time: Time):
    crud_neo4j.create_time(time.nome, time.cidade)
    return {"mensagem": "Time criado com sucesso!"}

@app.get("/times/")
def listar_times():
    return crud_neo4j.read_times()

@app.put("/times/{nome}")
def atualizar_time(nome: str, dados: UpdateTime):
    if not dados.cidade:
        raise HTTPException(status_code=400, detail="Nada para atualizar")
    result = crud_neo4j.update_time(nome, dados.cidade)
    if not result:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return {"atualizado": result}

@app.delete("/times/{nome}")
def deletar_time(nome: str):
    crud_neo4j.delete_time(nome)
    return {"mensagem": f"Time {nome} removido"}

# ================== ROTAS PARTIDAS ==================

@app.post("/partidas/")
def criar_partida(partida: Partida):
    crud_neo4j.create_partida(
        partida.id_partida, partida.time_casa, partida.time_fora,
        partida.data, partida.pontos_casa, partida.pontos_fora
    )
    return {"mensagem": "Partida criada com sucesso!"}

@app.get("/partidas/")
def listar_partidas():
    return crud_neo4j.read_partidas()

@app.put("/partidas/{id_partida}")
def atualizar_partida(id_partida: str, dados: UpdatePartida):
    if dados.pontos_casa is None and dados.pontos_fora is None:
        raise HTTPException(status_code=400, detail="Nada para atualizar")
    result = crud_neo4j.update_partida(id_partida, dados.pontos_casa, dados.pontos_fora)
    if not result:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return {"atualizado": result}

@app.delete("/partidas/{id_partida}")
def deletar_partida(id_partida: str):
    crud_neo4j.delete_partida(id_partida)
    return {"mensagem": f"Partida {id_partida} removida"}

# ================== ROTA ROOT ==================

@app.get("/")
def root():
    return {"mensagem": "API Neo4j funcionando!"}