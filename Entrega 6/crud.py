import re
import time
from bson import ObjectId
from database import (
    colecao_ofensiva,
    colecao_defensiva,
    colecao_jogadores,
    colecao_times,
    colecao_partidas,
    colecao_historico,
    get_from_cache,
    set_cache,
    flatten_dict
)

# ---------- Função auxiliar para serializar documentos ----------
def _serialize_doc(doc):
    if isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
            elif isinstance(v, dict):
                out[k] = _serialize_doc(v)
            elif isinstance(v, list):
                new_list = []
                for item in v:
                    if isinstance(item, dict):
                        new_list.append(_serialize_doc(item))
                    elif isinstance(item, ObjectId):
                        new_list.append(str(item))
                    else:
                        new_list.append(item)
                out[k] = new_list
            else:
                out[k] = v
        return out
    return doc

# ================================================================
# ================== CRUD Assíncrono para ofensivas ============
# ================================================================
async def read_estatistica_ofensiva_by_nome(nome: str):
    start = time.time()
    doc = await colecao_ofensiva.find_one({"nome": nome})
    elapsed = (time.time() - start) * 1000
    if doc:
        doc = _serialize_doc(doc)
        print(f"[MongoDB] {nome} encontrado em {elapsed:.2f} ms")
        cache_key = f"ofensiva:{nome}"
        await set_cache(cache_key, doc)
        return {"source": "mongo", "doc": doc}
    print(f"[MongoDB] {nome} não encontrado ({elapsed:.2f} ms)")
    return None

async def create_estatistica_ofensiva(data: dict):
    resultado = await colecao_ofensiva.insert_one(data)
    return str(resultado.inserted_id)

async def read_estatisticas_ofensiva():
    start = time.time()
    cursor = colecao_ofensiva.find()
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Estatísticas ofensivas lidas em {elapsed:.2f} ms")
    return resultados

async def update_estatistica_ofensiva(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = await colecao_ofensiva.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

async def delete_estatistica_ofensiva(nome: str):
    resultado = await colecao_ofensiva.delete_one({"nome": nome})
    return resultado.deleted_count

async def buscar_jogadores_com_pontos(min_pontos: int):
    start = time.time()
    cursor = colecao_ofensiva.find({"pontos": {"$gte": min_pontos}})
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Busca por jogadores com >= {min_pontos} pontos em {elapsed:.2f} ms")
    return resultados

# ================================================================
# ================== CRUD Assíncrono para defensivas ============
# ================================================================
async def read_estatistica_defensiva_by_nome(nome: str):
    start = time.time()
    doc = await colecao_defensiva.find_one({"nome": nome})
    elapsed = (time.time() - start) * 1000
    if doc:
        doc = _serialize_doc(doc)
        print(f"[MongoDB] {nome} encontrado em {elapsed:.2f} ms")
        cache_key = f"defensiva:{nome}"
        await set_cache(cache_key, doc)
        return {"source": "mongo", "doc": doc}
    print(f"[MongoDB] {nome} não encontrado ({elapsed:.2f} ms)")
    return None

async def create_estatistica_defensiva(data: dict):
    resultado = await colecao_defensiva.insert_one(data)
    return str(resultado.inserted_id)

async def read_estatisticas_defensiva():
    start = time.time()
    cursor = colecao_defensiva.find()
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Estatísticas defensivas lidas em {elapsed:.2f} ms")
    return resultados

async def update_estatistica_defensiva(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = await colecao_defensiva.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

async def delete_estatistica_defensiva(nome: str):
    resultado = await colecao_defensiva.delete_one({"nome": nome})
    return resultado.deleted_count

async def jogadores_com_muitos_rebotes_defensivos(min_rebotes: int):
    start = time.time()
    pipeline = [
        {"$match": {"rebotes_defensivos": {"$gte": min_rebotes}}},
        {"$sort": {"rebotes_defensivos": -1}},
        {"$project": {"_id": 0, "nome": 1, "rebotes_defensivos": 1}}
    ]
    cursor = colecao_defensiva.aggregate(pipeline)
    resultados = []
    async for doc in cursor:
        resultados.append(doc)
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Busca por jogadores com >= {min_rebotes} rebotes defensivos em {elapsed:.2f} ms")
    return resultados

# ================================================================
# ================== CRUD Assíncrono para jogadores ============
# ================================================================
async def read_jogador_by_nome(nome: str):
    start = time.time()
    doc = await colecao_jogadores.find_one({"nome": nome})
    elapsed = (time.time() - start) * 1000
    if doc:
        doc = _serialize_doc(doc)
        print(f"[MongoDB] {nome} encontrado em {elapsed:.2f} ms")
        cache_key = f"jogador:{nome.lower()}"
        await set_cache(cache_key, doc)
        return {"source": "mongo", "doc": doc}
    print(f"[MongoDB] {nome} não encontrado ({elapsed:.2f} ms)")
    return None

async def create_jogador(data: dict):
    """
    Espera receber o modelo completo de jogador, incluindo estatísticas ofensivas e defensivas.
    """
    jogador = {
        "nome": data["nome"],
        "idade": data["idade"],
        "altura": data["altura"],
        "peso": data["peso"],
        "posicao": data["posicao"],
        "nacionalidade": data["nacionalidade"],
        "ofensiva": data.get("ofensiva", {}),
        "defensiva": data.get("defensiva", {})
    }
    resultado = await colecao_jogadores.insert_one(jogador)
    return str(resultado.inserted_id)

async def read_jogadores():
    start = time.time()
    cursor = colecao_jogadores.find()
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Leitura de todos os jogadores em {elapsed:.2f} ms")
    return resultados

async def update_jogador(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = await colecao_jogadores.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

async def delete_jogador(nome: str):
    resultado = await colecao_jogadores.delete_one({"nome": nome})
    return resultado.deleted_count

# ================================================================
# ================== CRUD Assíncrono para times =================
# ================================================================
async def read_time_by_nome(nome: str):
    start = time.time()
    doc = await colecao_times.find_one({"nome": nome})
    elapsed = (time.time() - start) * 1000
    if doc:
        doc = _serialize_doc(doc)
        print(f"[MongoDB] {nome} encontrado em {elapsed:.2f} ms")
        cache_key = f"time:{nome}"
        await set_cache(cache_key, doc)
        return {"source": "mongo", "doc": doc}
    print(f"[MongoDB] {nome} não encontrado ({elapsed:.2f} ms)")
    return None

async def create_time(data: dict):
    resultado = await colecao_times.insert_one(data)
    return str(resultado.inserted_id)

async def read_times():
    start = time.time()
    cursor = colecao_times.find()
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Leitura de todos os times em {elapsed:.2f} ms")
    return resultados

async def update_time(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = await colecao_times.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

async def delete_time(nome: str):
    resultado = await colecao_times.delete_one({"nome": nome})
    return resultado.deleted_count

# ================================================================
# ================== CRUD Assíncrono para partidas ============
# ================================================================
async def partidas_entre_times(time_casa: str, time_fora: str, max_results: int = 50):
    cache_key = f"partidas:{time_casa}:{time_fora}"

    if not time_casa or not time_fora:
        raise ValueError("time_casa e time_fora devem ser informados")

    pat_mand = re.escape(time_casa)
    pat_visit = re.escape(time_fora)

    # -------- Consulta Mongo primeiro --------
    start = time.time()
    pipeline = [
        {"$match": {
            "time_casa": {"$regex": pat_mand, "$options": "i"},
            "time_fora": {"$regex": pat_visit, "$options": "i"}
        }},
        {"$project": {"_id": 1, "time_casa": 1, "time_fora": 1, "data": 1,
                      "local": 1, "placar_casa": 1, "placar_fora": 1}},
        {"$sort": {"data": 1}},
        {"$limit": max_results}
    ]
    cursor = colecao_partidas.aggregate(pipeline)
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    mongo_elapsed = (time.time() - start) * 1000

    if resultados:
        await set_cache(cache_key, {"swapped": False, "results": resultados})
        print(f"[MongoDB] Partidas entre {time_casa} x {time_fora} em {mongo_elapsed:.2f} ms")
        return {"source": "mongo", "doc": {"swapped": False, "results": resultados}}

    # -------- Busca invertida --------
    start = time.time()
    pipeline_swapped = [
        {"$match": {
            "time_casa": {"$regex": pat_visit, "$options": "i"},
            "time_fora": {"$regex": pat_mand, "$options": "i"}
        }},
        {"$project": {"_id": 1, "time_casa": 1, "time_fora": 1, "data": 1,
                      "local": 1, "placar_casa": 1, "placar_fora": 1}},
        {"$sort": {"data": 1}},
        {"$limit": max_results}
    ]
    cursor_swapped = colecao_partidas.aggregate(pipeline_swapped)
    resultados_swapped = []
    async for doc in cursor_swapped:
        resultados_swapped.append(_serialize_doc(doc))
    mongo_elapsed_swapped = (time.time() - start) * 1000

    if resultados_swapped:
        await set_cache(cache_key, {"swapped": True, "results": resultados_swapped})
        print(f"[MongoDB] Partidas invertidas entre {time_fora} x {time_casa} em {mongo_elapsed_swapped:.2f} ms")
        return {"source": "mongo", "doc": {"swapped": True, "results": resultados_swapped}}

    # Nenhum resultado encontrado
    return {"source": "mongo", "doc": {"swapped": False, "results": []}}

async def create_partida(data: dict):
    resultado = await colecao_partidas.insert_one(data)
    return str(resultado.inserted_id)

async def read_partidas():
    start = time.time()
    cursor = colecao_partidas.find()
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Leitura de todas as partidas em {elapsed:.2f} ms")
    return resultados

async def read_partida_by_id(partida_id: str):
    start = time.time()
    doc = await colecao_partidas.find_one({"_id": ObjectId(partida_id)})
    elapsed = (time.time() - start) * 1000
    if doc:
        doc = _serialize_doc(doc)
    print(f"[MongoDB] Partida {partida_id} lida em {elapsed:.2f} ms")
    return doc

async def update_partida(partida_id: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = await colecao_partidas.update_one({"_id": ObjectId(partida_id)}, {"$set": dados_formatados})
    return resultado.modified_count

async def delete_partida(partida_id: str):
    resultado = await colecao_partidas.delete_one({"_id": ObjectId(partida_id)})
    return resultado.deleted_count

# ================================================================
# ================== CRUD Assíncrono para histórico ============
# ================================================================
async def read_historico_by_nome(nome: str):
    start = time.time()
    doc = await colecao_historico.find_one({"nome": nome})
    elapsed = (time.time() - start) * 1000
    if doc:
        doc = _serialize_doc(doc)
        print(f"[MongoDB] Histórico {nome} lido em {elapsed:.2f} ms")
        cache_key = f"historico:{nome}"
        await set_cache(cache_key, doc)
        return {"source": "mongo", "doc": doc}
    print(f"[MongoDB] Histórico {nome} não encontrado ({elapsed:.2f} ms)")
    return None

async def create_historico(data: dict):
    resultado = await colecao_historico.insert_one(data)
    return str(resultado.inserted_id)

async def read_historico():
    start = time.time()
    cursor = colecao_historico.find()
    resultados = []
    async for doc in cursor:
        resultados.append(_serialize_doc(doc))
    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Leitura de todo histórico em {elapsed:.2f} ms")
    return resultados

async def update_historico(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = await colecao_historico.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

async def delete_historico(nome: str):
    resultado = await colecao_historico.delete_one({"nome": nome})
    return resultado.deleted_count