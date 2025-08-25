from fastapi import FastAPI, HTTPException, Query, Request
from typing import Optional
from models import (
    Jogador, UpdateJogador,
    Time, UpdateTime,
    Partida, UpdatePartida,
    HistoricoJogador, UpdateHistoricoJogador
)
import crud
from dotenv import load_dotenv
import os
import uvicorn

# -------------------- CONFIGURAÇÕES --------------------
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_STREAM_KEY = os.getenv("REDIS_STREAM_KEY", "nba_player_stats_stream")

app = FastAPI(title="NBA Desempenho API")

# -------------------- REDIS ASYNC --------------------
import redis.asyncio as redis

@app.on_event("startup")
async def startup():
    app.state.redis = await redis.from_url(REDIS_URL, decode_responses=True)
    print("Conexão Redis Estabelecida")

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()
    print("Conexão Redis Fechada")

def get_redis(request: Request):
    return request.app.state.redis

# -------------------- FUNÇÕES REDIS STREAM --------------------
async def add_to_stream_async(redis_client, nome: str, time: str, local_jogo: str, estatisticas: dict):
    evento = {
        "nome": nome,
        "time": time,
        "local_jogo": local_jogo,
        **estatisticas
    }
    await redis_client.xadd(REDIS_STREAM_KEY, evento)
    return evento

async def read_stream_async(redis_client, last_id="0", count=10):
    mensagens = await redis_client.xread({REDIS_STREAM_KEY: last_id}, count=count, block=0)
    return mensagens

# -------------------- ROTAS JOGADORES --------------------
@app.post("/jogadores/")
async def criar_jogador(jogador: Jogador):
    id = await crud.create_jogador(jogador.dict())
    return {"id": id}

@app.get("/jogadores/")
async def listar_jogadores():
    return await crud.read_jogadores()

@app.get("/jogadores/{nome}")
async def obter_jogador(nome: str):
    jogador = await crud.read_jogador_by_nome(nome)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador

@app.put("/jogadores/{nome}")
async def atualizar_jogador(nome: str, dados: UpdateJogador):
    mod = await crud.update_jogador(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return {"modificado": mod}

@app.delete("/jogadores/{nome}")
async def deletar_jogador(nome: str):
    deletado = await crud.delete_jogador(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return {"deletado": deletado}

# -------------------- ROTAS TIMES --------------------
@app.post("/times/")
async def criar_time(time: Time):
    id = await crud.create_time(time.dict())
    return {"id": id}

@app.get("/times/")
async def listar_times():
    return await crud.read_times()

@app.get("/times/{nome}")
async def obter_time(nome: str):
    time = await crud.read_time_by_nome(nome)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return time

@app.put("/times/{nome}")
async def atualizar_time(nome: str, dados: UpdateTime):
    mod = await crud.update_time(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return {"modificado": mod}

@app.delete("/times/{nome}")
async def deletar_time(nome: str):
    deletado = await crud.delete_time(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return {"deletado": deletado}

# -------------------- ROTAS PARTIDAS --------------------
@app.post("/partidas/")
async def criar_partida(partida: Partida):
    id = await crud.create_partida(partida.dict())
    return {"id": id}

@app.get("/partidas/")
async def listar_partidas():
    return await crud.read_partidas()

@app.get("/partidas/{id_partida}")
async def obter_partida(id_partida: str):
    partida = await crud.read_partida_by_id(id_partida)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida

@app.put("/partidas/{id_partida}")
async def atualizar_partida(id_partida: str, dados: UpdatePartida):
    mod = await crud.update_partida(id_partida, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return {"modificado": mod}

@app.delete("/partidas/{id_partida}")
async def deletar_partida(id_partida: str):
    deletado = await crud.delete_partida(id_partida)
    if not deletado:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return {"deletado": deletado}

@app.get("/partidas/confrontos/")
async def listar_partidas_confronto(
    time_casa: str = Query(..., description="Nome (ou parte) do time casa"),
    time_fora: str = Query(..., description="Nome (ou parte) do time fora"),
    max_results: Optional[int] = Query(50, ge=1, le=500, description="Número máximo de resultados retornados")
):
    try:
        resp = await crud.partidas_entre_times(time_casa, time_fora, max_results=max_results)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

    if not resp or not resp.get("doc") or not resp["doc"].get("results"):
        raise HTTPException(status_code=404, detail=f"Nenhuma partida encontrada entre '{time_casa}' e '{time_fora}'.")

    return resp

# -------------------- ROTAS HISTÓRICO --------------------
@app.post("/historico/")
async def criar_historico(historico: HistoricoJogador):
    id = await crud.create_historico(historico.dict())
    return {"id": id}

@app.get("/historico/")
async def listar_historico():
    return await crud.read_historico()

@app.get("/historico/{nome}")
async def obter_historico(nome: str):
    historico = await crud.read_historico_by_nome(nome)
    if not historico:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return historico

@app.put("/historico/{nome}")
async def atualizar_historico(nome: str, dados: UpdateHistoricoJogador):
    mod = await crud.update_historico(nome, dados.dict(exclude_unset=True))
    if not mod:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return {"modificado": mod}

@app.delete("/historico/{nome}")
async def deletar_historico(nome: str):
    deletado = await crud.delete_historico(nome)
    if not deletado:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return {"deletado": deletado}

# -------------------- ROTAS REDIS STREAM --------------------
@app.post("/stream/game-stats/")
async def registrar_estatistica_stream(jogador: Jogador, request: Request):
    """
    Registra estatísticas do jogador no Redis Stream.
    Usa os dados ofensivos e defensivos do modelo Jogador.
    """
    redis_client = get_redis(request)
    estatisticas = {**jogador.ofensiva.dict(), **jogador.defensiva.dict()}
    evento = await add_to_stream_async(
        redis_client, jogador.nome, jogador.time, jogador.local_jogo, estatisticas
    )
    return {"mensagem": "Estatística registrada no Stream", "evento": evento}


@app.get("/stream/game-stats/")
async def consultar_estatisticas_stream(request: Request, last_id: str = "0", count: int = 10):
    """
    Consulta eventos do Redis Stream.
    - last_id="0" → lê desde o começo (histórico completo)
    - last_id="$" → lê apenas novos eventos (modo real-time)
    - count → quantidade máxima de eventos retornados
    """
    redis_client = get_redis(request)
    eventos = await read_stream_async(redis_client, last_id=last_id, count=count)
    return {"eventos": eventos}

# -------------------- ROTA RAIZ --------------------
@app.get("/")
async def root():
    return {"message": "API NBA funcionando!"}

# -------------------- EXECUÇÃO --------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )