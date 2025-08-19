from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import json
import redis.asyncio as redis
import certifi  # para TLS/SSL seguro
import time

load_dotenv()

# -------------------- MONGO ASSÍNCRONO --------------------
MONGO_URI = os.getenv("host")
mongo_client = AsyncIOMotorClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
db = mongo_client["desempenhoJogadoresNBA"]

# -------------------- COLEÇÕES --------------------
colecao_ofensiva = db["ofensiva"] if db is not None else None
colecao_defensiva = db["defensiva"] if db is not None else None
colecao_jogadores = db["jogadores"] if db is not None else None
colecao_times = db["times"] if db is not None else None
colecao_partidas = db["partidas"] if db is not None else None
colecao_historico = db["historico"] if db is not None else None

# -------------------- REDIS --------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
rds = redis.from_url(REDIS_URL, decode_responses=True)

async def get_from_cache(key: str):
    """
    Recupera dados do Redis e loga tempo de execução.
    """
    start = time.time()
    data = await rds.get(key)
    elapsed = (time.time() - start) * 1000  # ms
    if data:
        print(f"[Redis] {key} encontrado em {elapsed:.2f} ms")
        return json.loads(data)
    print(f"[Redis] {key} não encontrado ({elapsed:.2f} ms)")
    return None

async def set_cache(key: str, value, ttl: int = 300):
    """
    Salva dados no Redis e loga tempo de execução.
    """
    start = time.time()
    await rds.set(key, json.dumps(value), ex=ttl)
    elapsed = (time.time() - start) * 1000
    print(f"[Redis] {key} salvo em cache em {elapsed:.2f} ms")

def get_redis():
    return rds

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# -------------------- AUXILIAR PARA MONGO COM LOG --------------------
async def mongo_find_one(collection, query, cache_key: str = None):
    """
    Busca documento no MongoDB primeiro e opcionalmente salva no Redis.
    Retorna dict com 'source' e 'doc'.
    """
    # Tenta buscar no Redis primeiro (opcional)
    if cache_key:
        doc = await get_from_cache(cache_key)
        if doc:
            return {"source": "redis", "doc": doc}

    # Busca no MongoDB
    start = time.time()
    doc = await collection.find_one(query)
    elapsed = (time.time() - start) * 1000
    if doc:
        # Serializa _id
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        print(f"[MongoDB] {query} encontrado em {elapsed:.2f} ms")
        # Salva no Redis
        if cache_key:
            await set_cache(cache_key, doc)
        return {"source": "mongo", "doc": doc}

    print(f"[MongoDB] {query} não encontrado ({elapsed:.2f} ms)")
    return None

# -------------------- NOVAS FUNÇÕES AUXILIARES --------------------
async def mongo_find(collection, query={}, cache_key: str = None, limit: int = 0, sort=None):
    """
    Busca múltiplos documentos no MongoDB e opcionalmente salva no Redis.
    """
    # Tenta buscar no Redis
    if cache_key:
        doc = await get_from_cache(cache_key)
        if doc:
            return {"source": "redis", "doc": doc}

    start = time.time()
    cursor = collection.find(query)
    if sort:
        cursor = cursor.sort(sort)
    if limit > 0:
        cursor = cursor.limit(limit)

    resultados = []
    async for doc in cursor:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        resultados.append(doc)

    elapsed = (time.time() - start) * 1000
    print(f"[MongoDB] Busca {query} em {elapsed:.2f} ms")
    if resultados and cache_key:
        await set_cache(cache_key, resultados)
    return {"source": "mongo", "doc": resultados}