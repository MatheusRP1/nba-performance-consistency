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

def read_jogadores_por_time(time_nome):
    """Lista jogadores de um time específico."""
    with driver.session() as session:
        query = """
        MATCH (t:Time {nome: $time_nome})<-[:PERTENCE_A]-(j:Jogador)
        RETURN j.nome AS nome, j.posicao AS posicao
        """
        result = session.run(query, time_nome=time_nome)
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
    """Cria um time."""
    with driver.session() as session:
        query = """
        MERGE (t:Time {nome: $nome})
        SET t.cidade = $cidade
        """
        session.run(query, nome=nome, cidade=cidade)

def read_times():
    """Lista todos os times cadastrados."""
    with driver.session() as session:
        query = """
        MATCH (t:Time)
        RETURN t.nome AS nome, t.cidade AS cidade
        """
        result = session.run(query)
        return [record.data() for record in result]

def update_time(nome, nova_cidade):
    """Atualiza a cidade de um time."""
    with driver.session() as session:
        query = """
        MATCH (t:Time {nome: $nome})
        SET t.cidade = $nova_cidade
        RETURN t.nome AS nome, t.cidade AS cidade
        """
        result = session.run(query, nome=nome, nova_cidade=nova_cidade)
        return result.single()

def delete_time(nome):
    """Remove um time (e seus relacionamentos)."""
    with driver.session() as session:
        query = """
        MATCH (t:Time {nome: $nome})
        DETACH DELETE t
        """
        session.run(query, nome=nome)


# ================== FUNÇÕES DE PARTIDA ==================

def create_partida(id_partida, time_casa, time_fora, data, pontos_casa, pontos_fora):
    """Cria uma partida entre dois times."""
    with driver.session() as session:
        query = """
        MERGE (p:Partida {id: $id_partida})
        SET p.data = $data, p.pontos_casa = $pontos_casa, p.pontos_fora = $pontos_fora
        WITH p
        MATCH (c:Time {nome: $time_casa})
        MATCH (f:Time {nome: $time_fora})
        MERGE (c)-[:MANDANTE]->(p)
        MERGE (f)-[:VISITANTE]->(p)
        """
        session.run(query, id_partida=id_partida, time_casa=time_casa, time_fora=time_fora, data=data,
                    pontos_casa=pontos_casa, pontos_fora=pontos_fora)

def read_partidas():
    """Lista todas as partidas cadastradas."""
    with driver.session() as session:
        query = """
        MATCH (c:Time)-[:MANDANTE]->(p:Partida)<-[:VISITANTE]-(f:Time)
        RETURN p.id AS id, p.data AS data, 
               c.nome AS time_casa, f.nome AS time_fora,
               p.pontos_casa AS pontos_casa, p.pontos_fora AS pontos_fora
        """
        result = session.run(query)
        return [record.data() for record in result]

def update_partida(id_partida, pontos_casa, pontos_fora):
    """Atualiza o placar de uma partida."""
    with driver.session() as session:
        query = """
        MATCH (p:Partida {id: $id_partida})
        SET p.pontos_casa = $pontos_casa, p.pontos_fora = $pontos_fora
        RETURN p.id AS id, p.pontos_casa AS pontos_casa, p.pontos_fora AS pontos_fora
        """
        result = session.run(query, id_partida=id_partida, pontos_casa=pontos_casa, pontos_fora=pontos_fora)
        return result.single()

def delete_partida(id_partida):
    """Remove uma partida do banco."""
    with driver.session() as session:
        query = """
        MATCH (p:Partida {id: $id_partida})
        DETACH DELETE p
        """
        session.run(query, id_partida=id_partida)


# ================== ENCERRAR CONEXÃO ==================

def close_driver():
    """Fecha a conexão com o Neo4j."""
    driver.close()