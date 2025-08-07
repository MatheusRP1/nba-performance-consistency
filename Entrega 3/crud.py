from bson import ObjectId
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

# ================================================================
# ================== CRUD para partidas =========================
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