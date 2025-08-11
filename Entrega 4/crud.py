import re
from bson import ObjectId
from database import db
from database import (
    colecao_ofensiva,
    colecao_defensiva,
    colecao_jogadores,
    colecao_times,
    colecao_partidas,
    colecao_historico
)

# ---------- Função auxiliar para atualizar campos aninhados ----------
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# ================================================================
# ================== CRUD para estatísticas ofensivas ===========
# ================================================================
def create_estatistica_ofensiva(data: dict):
    resultado = colecao_ofensiva.insert_one(data)
    return str(resultado.inserted_id)

def read_estatisticas_ofensiva():
    return [{**doc, "_id": str(doc["_id"])} for doc in colecao_ofensiva.find()]

def read_estatistica_ofensiva_by_nome(nome: str):
    doc = colecao_ofensiva.find_one({"nome": nome})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_estatistica_ofensiva(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = colecao_ofensiva.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

def delete_estatistica_ofensiva(nome: str):
    resultado = colecao_ofensiva.delete_one({"nome": nome})
    return resultado.deleted_count

def buscar_jogadores_com_pontos(min_pontos: int):
    """
    Busca jogadores ofensivos que fizeram pontos >= min_pontos,
    utilizando índice no campo 'pontos'.
    """
    cursor = colecao_ofensiva.find({"pontos": {"$gte": min_pontos}})
    return [{**doc, "_id": str(doc["_id"])} for doc in cursor]

# ================================================================
# ================== CRUD para estatísticas defensivas ===========
# ================================================================
def create_estatistica_defensiva(data: dict):
    resultado = colecao_defensiva.insert_one(data)
    return str(resultado.inserted_id)

def read_estatisticas_defensiva():
    return [{**doc, "_id": str(doc["_id"])} for doc in colecao_defensiva.find()]

def read_estatistica_defensiva_by_nome(nome: str):
    doc = colecao_defensiva.find_one({"nome": nome})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_estatistica_defensiva(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = colecao_defensiva.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

def delete_estatistica_defensiva(nome: str):
    resultado = colecao_defensiva.delete_one({"nome": nome})
    return resultado.deleted_count

# === Nova operação usando aggregation: jogadores com muitos rebotes defensivos ===
def jogadores_com_muitos_rebotes_defensivos(min_rebotes: int):
    pipeline = [
        {"$match": {"rebotes_defensivos": {"$gte": min_rebotes}}},
        {"$sort": {"rebotes_defensivos": -1}},
        {"$project": {"_id": 0, "nome": 1, "rebotes_defensivos": 1}}
    ]
    resultados = colecao_defensiva.aggregate(pipeline)
    return list(resultados)

# ================================================================
# ================== CRUD para jogadores ========================
# ================================================================
def create_jogador(data: dict):
    resultado = colecao_jogadores.insert_one(data)
    return str(resultado.inserted_id)

def read_jogadores():
    return [{**doc, "_id": str(doc["_id"])} for doc in colecao_jogadores.find()]

def read_jogador_by_nome(nome: str):
    doc = colecao_jogadores.find_one({"nome": nome})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_jogador(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = colecao_jogadores.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

def delete_jogador(nome: str):
    resultado = colecao_jogadores.delete_one({"nome": nome})
    return resultado.deleted_count

# ================================================================
# ================== CRUD para times ============================
# ================================================================
def create_time(data: dict):
    resultado = colecao_times.insert_one(data)
    return str(resultado.inserted_id)

def read_times():
    return [{**doc, "_id": str(doc["_id"])} for doc in colecao_times.find()]

def read_time_by_nome(nome: str):
    doc = colecao_times.find_one({"nome": nome})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_time(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = colecao_times.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

def delete_time(nome: str):
    resultado = colecao_times.delete_one({"nome": nome})
    return resultado.deleted_count

# utilitário para serializar documentos retornados pelo Mongo (converte ObjectId para str)
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

def partidas_entre_times(time_casa: str, time_fora: str, max_results: int = 50):
    """
    Busca partidas entre dois times. Faz match parcial (case-insensitive) usando regex escapado.
    Se não encontrar nada com a ordem (casa, fora), tenta inverter (casa, fora).
    Retorna lista de documentos serializados.
    """
    if not time_casa or not time_fora:
        raise ValueError("time_casa e time_fora devem ser informados")

    # escapar termos do usuário para evitar regex injection
    pat_mand = re.escape(time_casa)
    pat_visit = re.escape(time_fora)

    pipeline = [
        {
            "$match": {
                "time_casa": {"$regex": pat_mand, "$options": "i"},
                "time_fora": {"$regex": pat_visit, "$options": "i"}
            }
        },
        {
            "$project": {
                # ajustar campos conforme seu esquema em 'partidas'
                "_id": 1,
                "time_casa": 1,
                "time_fora": 1,
                "data": 1,
                "local": 1,
                "placar_casa": 1,
                "placar_fora": 1
            }
        },
        {"$sort": {"data": 1}},
        {"$limit": max_results}
    ]

    resultados = list(colecao_partidas.aggregate(pipeline))
    resultados = [_serialize_doc(d) for d in resultados]

    # se vazio, tenta inverter (algumas vezes os dados podem estar no sentido inverso)
    if not resultados:
        pipeline_swapped = [
            {
                "$match": {
                    "time_casa": {"$regex": pat_visit, "$options": "i"},
                    "time_fora": {"$regex": pat_mand, "$options": "i"}
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "time_casa": 1,
                    "time_fora": 1,
                    "data": 1,
                    "local": 1,
                    "placar_casa": 1,
                    "placar_fora": 1
                }
            },
            {"$sort": {"data": 1}},
            {"$limit": max_results}
        ]
        resultados_swapped = list(colecao_partidas.aggregate(pipeline_swapped))
        resultados_swapped = [_serialize_doc(d) for d in resultados_swapped]
        # indica que foi buscado invertido retornando os documentos (se houver)
        if resultados_swapped:
            return {"swapped": True, "results": resultados_swapped}

    return {"swapped": False, "results": resultados}

# ================================================================
# ================== CRUD para partidas ==========================
# ================================================================
def create_partida(data: dict):
    resultado = colecao_partidas.insert_one(data)
    return str(resultado.inserted_id)

def read_partidas():
    return [{**doc, "_id": str(doc["_id"])} for doc in colecao_partidas.find()]

def read_partida_by_id(partida_id: str):
    doc = colecao_partidas.find_one({"_id": ObjectId(partida_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_partida(partida_id: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = colecao_partidas.update_one({"_id": ObjectId(partida_id)}, {"$set": dados_formatados})
    return resultado.modified_count

def delete_partida(partida_id: str):
    resultado = colecao_partidas.delete_one({"_id": ObjectId(partida_id)})
    return resultado.deleted_count

# ================================================================
# ================== CRUD para histórico de jogador =============
# ================================================================
def create_historico(data: dict):
    resultado = colecao_historico.insert_one(data)
    return str(resultado.inserted_id)

def read_historico():
    return [{**doc, "_id": str(doc["_id"])} for doc in colecao_historico.find()]

def read_historico_by_nome(nome: str):
    doc = colecao_historico.find_one({"nome": nome})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_historico(nome: str, novos_dados: dict):
    dados_formatados = flatten_dict(novos_dados)
    resultado = colecao_historico.update_one({"nome": nome}, {"$set": dados_formatados})
    return resultado.modified_count

def delete_historico(nome: str):
    resultado = colecao_historico.delete_one({"nome": nome})
    return resultado.deleted_count