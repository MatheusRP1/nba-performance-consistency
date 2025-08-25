import os
import redis
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Pegar as variáveis de ambiente
REDIS_URL = os.getenv("REDIS_URL")
REDIS_STREAM_KEY = os.getenv("REDIS_STREAM_KEY", "nba_player_stats_stream")

# Criar cliente Redis
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def add_to_stream(nome: str, time: str, local_jogo: str, estatisticas: dict):
    """
    Adiciona estatísticas de um jogador ao Redis Stream.
    - nome: nome do jogador
    - time: time do jogador
    - local_jogo: 'casa' ou 'fora'
    - estatisticas: dicionário com métricas (pontos, rebotes, assistências etc.)
    """
    evento = {
        "nome": nome,
        "time": time,
        "local_jogo": local_jogo,
        **estatisticas
    }
    redis_client.xadd(REDIS_STREAM_KEY, evento)
    return evento


def read_stream(last_id="0", count=10):
    """
    Lê eventos do Redis Stream.
    - last_id="0" → lê desde o começo (histórico completo).
    - last_id="$" → lê apenas novos eventos (modo real-time).
    - count → número máximo de eventos retornados.
    """
    mensagens = redis_client.xread({REDIS_STREAM_KEY: last_id}, count=count, block=0)
    return mensagens