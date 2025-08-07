from fastapi import FastAPI, HTTPException
from models import (
    EstatisticaOfensiva,
    UpdateEstatisticaOfensiva,
    EstatisticaDefensiva,
    UpdateEstatisticaDefensiva,
    Jogador,
    UpdateJogador,
    Time,
    UpdateTime,
    Partida,
    UpdatePartida,
    HistoricoJogador,
    UpdateHistoricoJogador
)
import crud

app = FastAPI(title="NBA Desempenho API")

# -------------------- ROTAS OFENSIVAS --------------------
@app.post("/ofensivos/")
def criar_estatistica_ofensiva(estatistica: EstatisticaOfensiva):
    id = crud.create_estatistica_ofensiva(estatistica.dict())
    return {"id": id}

@app.get("/ofensivos/")
def listar_estatisticas_ofensivas():
    return crud.read_estatisticas_ofensiva()

@app.get("/ofensivos/{nome}")
def obter_estatistica_ofensiva(nome: str):
    estatistica = crud.read_estatistica_ofensiva_by_nome(nome)
    if not estatistica:
        raise HTTPException(status_code=404, detail="Jogador não encontrado (ofensivo)")
    return estatistica

@app.put("/ofensivos/{nome}")
def atualizar_estatistica_ofensiva(nome: str, dados: UpdateEstatisticaOfensiva):
    mod = crud.update_estatistica_ofensiva(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Jogador não encontrado (ofensivo)")
    return {"modificado": mod}

@app.delete("/ofensivos/{nome}")
def deletar_estatistica_ofensiva(nome: str):
    deletado = crud.delete_estatistica_ofensiva(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Jogador não encontrado (ofensivo)")
    return {"deletado": deletado}

@app.get("/ofensivos/pontos/maior_igual/{min_pontos}")
def buscar_jogadores_com_pontos(min_pontos: int):
    jogadores = crud.buscar_jogadores_com_pontos(min_pontos)
    if not jogadores:
        raise HTTPException(status_code=404, detail=f"Nenhum jogador encontrado com {min_pontos}+ pontos.")
    return jogadores

# -------------------- ROTAS DEFENSIVAS --------------------
@app.post("/defensivos/")
def criar_estatistica_defensiva(estatistica: EstatisticaDefensiva):
    id = crud.create_estatistica_defensiva(estatistica.dict())
    return {"id": id}

@app.get("/defensivos/")
def listar_estatisticas_defensivas():
    return crud.read_estatisticas_defensiva()

@app.get("/defensivos/{nome}")
def obter_estatistica_defensiva(nome: str):
    estatistica = crud.read_estatistica_defensiva_by_nome(nome)
    if not estatistica:
        raise HTTPException(status_code=404, detail="Jogador não encontrado (defensivo)")
    return estatistica

@app.put("/defensivos/{nome}")
def atualizar_estatistica_defensiva(nome: str, dados: UpdateEstatisticaDefensiva):
    mod = crud.update_estatistica_defensiva(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Jogador não encontrado (defensivo)")
    return {"modificado": mod}

@app.delete("/defensivos/{nome}")
def deletar_estatistica_defensiva(nome: str):
    deletado = crud.delete_estatistica_defensiva(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Jogador não encontrado (defensivo)")
    return {"deletado": deletado}

# -------------------- ROTAS JOGADORES --------------------
@app.post("/jogadores/")
def criar_jogador(jogador: Jogador):
    id = crud.create_jogador(jogador.dict())
    return {"id": id}

@app.get("/jogadores/")
def listar_jogadores():
    return crud.read_jogadores()

@app.get("/jogadores/{nome}")
def obter_jogador(nome: str):
    jogador = crud.read_jogador_by_nome(nome)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador

@app.put("/jogadores/{nome}")
def atualizar_jogador(nome: str, dados: UpdateJogador):
    mod = crud.update_jogador(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return {"modificado": mod}

@app.delete("/jogadores/{nome}")
def deletar_jogador(nome: str):
    deletado = crud.delete_jogador(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return {"deletado": deletado}

# -------------------- ROTAS TIMES --------------------
@app.post("/times/")
def criar_time(time: Time):
    id = crud.create_time(time.dict())
    return {"id": id}

@app.get("/times/")
def listar_times():
    return crud.read_times()

@app.get("/times/{nome}")
def obter_time(nome: str):
    time = crud.read_time_by_nome(nome)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return time

@app.put("/times/{nome}")
def atualizar_time(nome: str, dados: UpdateTime):
    mod = crud.update_time(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return {"modificado": mod}

@app.delete("/times/{nome}")
def deletar_time(nome: str):
    deletado = crud.delete_time(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return {"deletado": deletado}

# -------------------- ROTAS PARTIDAS --------------------
@app.post("/partidas/")
def criar_partida(partida: Partida):
    id = crud.create_partida(partida.dict())
    return {"id": id}

@app.get("/partidas/")
def listar_partidas():
    return crud.read_partidas()

@app.get("/partidas/{id_partida}")
def obter_partida(id_partida: str):
    partida = crud.read_partida_by_id(id_partida)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida

@app.put("/partidas/{id_partida}")
def atualizar_partida(id_partida: str, dados: UpdatePartida):
    mod = crud.update_partida(id_partida, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return {"modificado": mod}

@app.delete("/partidas/{id_partida}")
def deletar_partida(id_partida: str):
    deletado = crud.delete_partida(id_partida)
    if not deletado:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return {"deletado": deletado}

# -------------------- ROTAS HISTÓRICO --------------------
@app.post("/historico/")
def criar_historico(historico: HistoricoJogador):
    id = crud.create_historico(historico.dict())
    return {"id": id}

@app.get("/historico/")
def listar_historico():
    return crud.read_historico()

@app.get("/historico/{nome}")
def obter_historico(nome: str):
    historico = crud.read_historico_by_nome(nome)
    if not historico:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return historico

@app.put("/historico/{nome}")
def atualizar_historico(nome: str, dados: UpdateHistoricoJogador):
    mod = crud.update_historico(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return {"modificado": mod}

@app.delete("/historico/{nome}")
def deletar_historico(nome: str):
    deletado = crud.delete_historico(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return {"deletado": deletado}