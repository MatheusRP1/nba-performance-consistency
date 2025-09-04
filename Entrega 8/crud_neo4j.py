import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# ================== CONFIGURAÇÃO ==================
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# ================== FUNÇÕES DE JOGADOR ==================

def create_jogador(nome, posicao, time_nome):
    """Cria um jogador e o associa a um time."""
    with driver.session() as session:
        query = """
        MERGE (j:Jogador {nome: $nome})
        SET j.posicao = $posicao
        WITH j
        MERGE (t:Time {nome: $time_nome})
        MERGE (j)-[:PERTENCE_A]->(t)
        """
        session.run(query, nome=nome, posicao=posicao, time_nome=time_nome)

def read_jogadores():
    """Lista todos os jogadores cadastrados."""
    with driver.session() as session:
        query = """
        MATCH (j:Jogador)-[:PERTENCE_A]->(t:Time)
        RETURN j.nome AS nome, j.posicao AS posicao, t.nome AS time
        """
        result = session.run(query)
        return [record.data() for record in result]

def update_jogador_posicao(nome, nova_posicao):
    """Atualiza a posição de um jogador."""
    with driver.session() as session:
        query = """
        MATCH (j:Jogador {nome: $nome})
        SET j.posicao = $nova_posicao
        RETURN j.nome AS nome, j.posicao AS posicao
        """
        result = session.run(query, nome=nome, nova_posicao=nova_posicao)
        return result.single()

def delete_jogador(nome):
    """Remove um jogador do banco."""
    with driver.session() as session:
        query = """
        MATCH (j:Jogador {nome: $nome})
        DETACH DELETE j
        """
        session.run(query, nome=nome)

# ================== FUNÇÕES DE TIME ==================

def create_time(nome, cidade):
    with driver.session() as session:
        query = """
        MERGE (t:Time {nome: $nome})
        SET t.cidade = $cidade
        """
        session.run(query, nome=nome, cidade=cidade)

def read_times():
    with driver.session() as session:
        query = "MATCH (t:Time) RETURN t.nome AS nome, t.cidade AS cidade"
        result = session.run(query)
        return [record.data() for record in result]

def update_time(nome, nova_cidade):
    with driver.session() as session:
        query = """
        MATCH (t:Time {nome: $nome})
        SET t.cidade = $nova_cidade
        RETURN t.nome AS nome, t.cidade AS cidade
        """
        result = session.run(query, nome=nome, nova_cidade=nova_cidade)
        return result.single()

def delete_time(nome):
    with driver.session() as session:
        query = "MATCH (t:Time {nome: $nome}) DETACH DELETE t"
        session.run(query, nome=nome)

# ================== FUNÇÕES DE PARTIDA ==================

def create_partida(id_partida, time_casa, time_fora, data, pontos_casa, pontos_fora):
    with driver.session() as session:
        query = """
        MERGE (p:Partida {id: $id_partida})
        SET p.data = $data, p.pontos_casa = $pontos_casa, p.pontos_fora = $pontos_fora
        WITH p
        MATCH (c:Time {nome: $time_casa})
        MATCH (f:Time {nome: $time_fora})
        MERGE (c)-[:JOGA_EM]->(p)
        MERGE (f)-[:JOGA_EM]->(p)
        """
        session.run(query, id_partida=id_partida, time_casa=time_casa, time_fora=time_fora,
                    data=data, pontos_casa=pontos_casa, pontos_fora=pontos_fora)

def read_partidas():
    with driver.session() as session:
        query = """
        MATCH (c:Time)-[:JOGA_EM]->(p:Partida)<-[:JOGA_EM]-(f:Time)
        RETURN p.id AS id, p.data AS data,
               c.nome AS time_casa, f.nome AS time_fora,
               p.pontos_casa AS pontos_casa, p.pontos_fora AS pontos_fora
        """
        result = session.run(query)
        return [record.data() for record in result]

def update_partida(id_partida, pontos_casa, pontos_fora):
    with driver.session() as session:
        query = """
        MATCH (p:Partida {id: $id_partida})
        SET p.pontos_casa = $pontos_casa, p.pontos_fora = $pontos_fora
        RETURN p.id AS id, p.pontos_casa AS pontos_casa, p.pontos_fora AS pontos_fora
        """
        result = session.run(query, id_partida=id_partida, pontos_casa=pontos_casa, pontos_fora=pontos_fora)
        return result.single()

def delete_partida(id_partida):
    with driver.session() as session:
        query = "MATCH (p:Partida {id: $id_partida}) DETACH DELETE p"
        session.run(query, id_partida=id_partida)

# ================== ANÁLISE: LOUVAIN ==================

def run_louvain():
    """
    Detecta comunidades usando Louvain, nos relacionamentos PERTENCE_A e JOGA_EM.
    Retorna lista de jogadores com a comunidade detectada.
    """
    with driver.session() as session:
        # Criar grafo projetado
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

        # Executar Louvain e escrever propriedade 'comunidade'
        session.run("""
        CALL gds.louvain.write('nbaGraph', {writeProperty: 'comunidade'})
        """)

        # Retornar jogadores com comunidades
        result = session.run("""
        MATCH (j:Jogador)-[:PERTENCE_A]->(t:Time)
        RETURN j.nome AS jogador, t.nome AS time, j.comunidade AS comunidade
        ORDER BY comunidade, jogador
        """)
        return [record.data() for record in result]

# ================== ENCERRAR CONEXÃO ==================

def close_driver():
    driver.close()