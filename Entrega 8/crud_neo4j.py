import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# ================== CONFIGURAÇÃO ==================
load_dotenv()

# Alternar entre AURA e SANDBOX via .env
USE_SANDBOX = os.getenv("USE_SANDBOX", "False").lower() == "true"

if USE_SANDBOX:
    NEO4J_URI = os.getenv("NEO4J_SANDBOX_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_SANDBOX_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_SANDBOX_PASSWORD")
    NEO4J_DATABASE = os.getenv("NEO4J_SANDBOX_DATABASE", "neo4j")
else:
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# ================== CRUD JOGADOR ==================
def create_jogador(nome, posicao, time_nome):
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("""
            MERGE (j:Jogador {nome: $nome})
            SET j.posicao = $posicao
            WITH j
            MERGE (t:Time {nome: $time_nome})
            MERGE (j)-[:PERTENCE_A]->(t)
        """, nome=nome, posicao=posicao, time_nome=time_nome)

def read_jogadores():
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("""
            MATCH (j:Jogador)-[:PERTENCE_A]->(t:Time)
            RETURN j.nome AS nome, j.posicao AS posicao, t.nome AS time
        """)
        return [record.data() for record in result]

def update_jogador_posicao(nome, nova_posicao):
    with driver.session(database=NEO4J_DATABASE) as session:
        return session.run("""
            MATCH (j:Jogador {nome: $nome})
            SET j.posicao = $nova_posicao
            RETURN j.nome AS nome, j.posicao AS posicao
        """, nome=nome, nova_posicao=nova_posicao).single()

def delete_jogador(nome):
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("MATCH (j:Jogador {nome: $nome}) DETACH DELETE j", nome=nome)

# ================== CRUD TIME ==================
def create_time(nome, cidade):
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("MERGE (t:Time {nome: $nome}) SET t.cidade = $cidade", nome=nome, cidade=cidade)

def read_times():
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("MATCH (t:Time) RETURN t.nome AS nome, t.cidade AS cidade")
        return [record.data() for record in result]

def update_time(nome, nova_cidade):
    with driver.session(database=NEO4J_DATABASE) as session:
        return session.run("""
            MATCH (t:Time {nome: $nome})
            SET t.cidade = $nova_cidade
            RETURN t.nome AS nome, t.cidade AS cidade
        """, nome=nome, nova_cidade=nova_cidade).single()

def delete_time(nome):
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("MATCH (t:Time {nome: $nome}) DETACH DELETE t", nome=nome)

# ================== CRUD PARTIDA ==================
def create_partida(id_partida, time_casa, time_fora, data, pontos_casa, pontos_fora):
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("""
            MERGE (p:Partida {id: $id_partida})
            SET p.data = $data, p.pontos_casa = $pontos_casa, p.pontos_fora = $pontos_fora
            WITH p
            MATCH (c:Time {nome: $time_casa})
            MATCH (f:Time {nome: $time_fora})
            MERGE (c)-[:JOGA_EM]->(p)
            MERGE (f)-[:JOGA_EM]->(p)
        """, id_partida=id_partida, time_casa=time_casa, time_fora=time_fora,
           data=data, pontos_casa=pontos_casa, pontos_fora=pontos_fora)

def read_partidas():
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("""
            MATCH (c:Time)-[:JOGA_EM]->(p:Partida)<-[:JOGA_EM]-(f:Time)
            RETURN p.id AS id, p.data AS data,
                   c.nome AS time_casa, f.nome AS time_fora,
                   p.pontos_casa AS pontos_casa, p.pontos_fora AS pontos_fora
        """)
        return [record.data() for record in result]

def update_partida(id_partida, pontos_casa, pontos_fora):
    with driver.session(database=NEO4J_DATABASE) as session:
        return session.run("""
            MATCH (p:Partida {id: $id_partida})
            SET p.pontos_casa = $pontos_casa, p.pontos_fora = $pontos_fora
            RETURN p.id AS id, p.pontos_casa AS pontos_casa, p.pontos_fora AS pontos_fora
        """, id_partida=id_partida, pontos_casa=pontos_casa, pontos_fora=pontos_fora).single()

def delete_partida(id_partida):
    with driver.session(database=NEO4J_DATABASE) as session:
        session.run("MATCH (p:Partida {id: $id_partida}) DETACH DELETE p", id_partida=id_partida)

# ================== ANÁLISE: LOUVAIN ==================
def run_louvain():
    with driver.session(database=NEO4J_DATABASE) as session:
        # 1️⃣ Fornecer credenciais Aura GDS
        if not USE_SANDBOX:
            session.run(f"""
            CALL gds.aura.api.credentials("{NEO4J_USERNAME}", "{NEO4J_PASSWORD}")
            """)

        # 2️⃣ Apagar projeção antiga (ignora se não existir)
        session.run("CALL gds.graph.drop('nbaGraph', false) YIELD graphName")

        # 3️⃣ Criar grafo projetado
        session.run("""
        CALL gds.graph.project(
            'nbaGraph',
            ['Jogador', 'Time', 'Partida'],
            {
                PERTENCE_A: {orientation: 'UNDIRECTED'},
                JOGA_EM: {orientation: 'UNDIRECTED'}
            }
        )
        """)

        # 4️⃣ Executar Louvain
        session.run("""
        CALL gds.louvain.write('nbaGraph', {writeProperty: 'comunidade'})
        """)

        # 5️⃣ Retornar jogadores com comunidades
        result = session.run("""
        MATCH (j:Jogador)-[:PERTENCE_A]->(t:Time)
        RETURN j.nome AS jogador, t.nome AS time, j.comunidade AS comunidade
        ORDER BY comunidade, jogador
        """)
        return [record.data() for record in result]

# ================== ENCERRAR DRIVER ==================
def close_driver():
    driver.close()