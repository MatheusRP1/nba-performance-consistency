import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from neo4j import GraphDatabase
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Carregar variáveis do .env
load_dotenv()

# ----- MongoDB -----
MONGO_URI = os.getenv("host")  
MONGO_DB = "desempenhoJogadoresNBA"   
MONGO_COLLECTION = "jogadores" 

# ----- Neo4j -----
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([MONGO_URI, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
    raise SystemExit("❌ Faltam variáveis no .env (verifique host, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD).")

# ----- Conexões -----
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
col = db[MONGO_COLLECTION]

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# ----- Funções Neo4j -----
def create_constraints(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Jogador) REQUIRE p.nome IS UNIQUE")
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Time) REQUIRE t.nome IS UNIQUE")
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Partida) REQUIRE m.id_partida IS UNIQUE")

def upsert_player_and_team(tx, player_nome, player_props, team_nome, team_props):
    tx.run(
        """
        MERGE (p:Jogador {nome: $player_nome})
        SET p += $player_props
        WITH p
        MERGE (t:Time {nome: $team_nome})
        SET t += $team_props
        MERGE (p)-[:PERTENCE_A]->(t)
        """,
        player_nome=player_nome,
        player_props=player_props or {},
        team_nome=team_nome,
        team_props=team_props or {}
    )

def upsert_partida_and_relations(tx, partida):
    # Converter _id para string
    id_partida = str(partida["_id"])
    tx.run(
        """
        MERGE (m:Partida {id_partida: $id_partida})
        SET m.data = $data, m.local = $local, m.placar_casa = $placar_casa, m.placar_fora = $placar_fora
        WITH m
        MERGE (c:Time {nome: $time_casa})
        MERGE (f:Time {nome: $time_fora})
        MERGE (c)-[:JOGA_EM]->(m)
        MERGE (f)-[:JOGA_EM]->(m)
        """,
        id_partida=id_partida,
        data=partida.get("data"),
        local=partida.get("local"),
        placar_casa=partida.get("placar_casa"),
        placar_fora=partida.get("placar_fora"),
        time_casa=partida.get("time_casa"),
        time_fora=partida.get("time_fora")
    )

# ----- Função principal -----
def main():
    logging.info("🚀 Criando constraints no Neo4j...")
    with driver.session() as session:
        session.execute_write(create_constraints)

    # Jogadores e times
    logging.info("📊 Coletando jogadores do MongoDB...")
    try:
        jogadores = col.distinct("nome")
    except Exception:
        docs = list(col.find({}, {"nome": 1, "time": 1}).limit(1000))
        jogadores = list({d.get("nome") for d in docs if d.get("nome")})

    logging.info(f"✅ Encontrados {len(jogadores)} jogadores.")

    with driver.session() as session:
        for nome in tqdm(jogadores, desc="Inserindo jogadores"):
            if not nome:
                continue
            doc = col.find_one({"nome": nome})
            if not doc:
                continue

            player_props = {}
            player_props['posicao'] = doc.get("posicao") or doc.get("position")
            if doc.get("player_id"):
                player_props['player_id'] = doc.get("player_id")
            player_props = {k: v for k, v in player_props.items() if v is not None}

            team_nome = doc.get("time") or doc.get("team") or "Desconhecido"
            team_props = {}
            if doc.get("team_id"):
                team_props['team_id'] = doc.get("team_id")
            if doc.get("conferencia"):
                team_props['conferencia'] = doc.get("conferencia")
            team_props = {k: v for k, v in team_props.items() if v is not None}

            session.execute_write(upsert_player_and_team, nome, player_props, team_nome, team_props)

    logging.info("🏀 Jogadores e times importados!")

    # Partidas
    logging.info("📊 Coletando partidas do MongoDB...")
    partidas_col = db.get_collection("partidas")
    partidas = list(partidas_col.find({}))
    logging.info(f"✅ Encontradas {len(partidas)} partidas.")

    with driver.session() as session:
        for partida in tqdm(partidas, desc="Inserindo partidas e relações"):
            session.execute_write(upsert_partida_and_relations, partida)

    logging.info("📌 Importação de partidas concluída!")

if __name__ == "__main__":
    main()