from database import (
    colecao_ofensiva,
    colecao_defensiva,
    colecao_jogadores,
    colecao_times,
    colecao_partidas,
    colecao_historico
)

# Jogadores + times + estatísticas (ofensiva e defensiva)
jogadores = [
    {
        "nome": "LeBron James",
        "time": "Los Angeles Lakers",
        "local_jogo": "fora",
        "ofensiva": {
            "pontos": 27,
            "bolas_3_convertidas": 4,
            "lances_livres_convertidos": 8,
            "aproveitamento_lance_livre": 73.5,
            "aproveitamento_bola_3": 34.2,
            "assistencias": 9,
            "rebotes_ofensivos": 3,
            "eficiencia": 30.2,
            "field_goal_percentage": 50.1,
            "toques_bola": 85,
            "minutos_jogados": 35.4
        },
        "defensiva": {
            "rebotes_defensivos": 7,
            "roubos_bola": 1,
            "bloqueios": 1,
            "turnovers": 4,
            "faltas": 2,
            "eficiencia": 29.5,
            "minutos_jogados": 35.4
        }
    },
    {
        "nome": "Giannis Antetokounmpo",
        "time": "Milwaukee Bucks",
        "local_jogo": "casa",
        "ofensiva": {
            "pontos": 31,
            "bolas_3_convertidas": 1,
            "lances_livres_convertidos": 7,
            "aproveitamento_lance_livre": 68.9,
            "aproveitamento_bola_3": 27.8,
            "assistencias": 7,
            "rebotes_ofensivos": 5,
            "eficiencia": 35.1,
            "field_goal_percentage": 56.2,
            "toques_bola": 90,
            "minutos_jogados": 34.1
        },
        "defensiva": {
            "rebotes_defensivos": 9,
            "roubos_bola": 2,
            "bloqueios": 3,
            "turnovers": 3,
            "faltas": 3,
            "eficiencia": 33.9,
            "minutos_jogados": 34.1
        }
    },
    {
        "nome": "Stephen Curry",
        "time": "Golden State Warriors",
        "local_jogo": "fora",
        "ofensiva": {
            "pontos": 33,
            "bolas_3_convertidas": 7,
            "lances_livres_convertidos": 10,
            "aproveitamento_lance_livre": 91.3,
            "aproveitamento_bola_3": 42.5,
            "assistencias": 6,
            "rebotes_ofensivos": 1,
            "eficiencia": 34.0,
            "field_goal_percentage": 52.7,
            "toques_bola": 88,
            "minutos_jogados": 36.0
        },
        "defensiva": {
            "rebotes_defensivos": 5,
            "roubos_bola": 1,
            "bloqueios": 0,
            "turnovers": 3,
            "faltas": 1,
            "eficiencia": 30.4,
            "minutos_jogados": 36.0
        }
    },
    {
        "nome": "Nikola Jokic",
        "time": "Denver Nuggets",
        "local_jogo": "casa",
        "ofensiva": {
            "pontos": 28,
            "bolas_3_convertidas": 3,
            "lances_livres_convertidos": 7,
            "aproveitamento_lance_livre": 83.0,
            "aproveitamento_bola_3": 35.0,
            "assistencias": 10,
            "rebotes_ofensivos": 4,
            "eficiencia": 36.5,
            "field_goal_percentage": 57.8,
            "toques_bola": 92,
            "minutos_jogados": 34.2
        },
        "defensiva": {
            "rebotes_defensivos": 11,
            "roubos_bola": 1,
            "bloqueios": 1,
            "turnovers": 2,
            "faltas": 2,
            "eficiencia": 32.8,
            "minutos_jogados": 34.2
        }
    },
    {
        "nome": "Kevin Durant",
        "time": "Phoenix Suns",
        "local_jogo": "fora",
        "ofensiva": {
            "pontos": 30,
            "bolas_3_convertidas": 5,
            "lances_livres_convertidos": 9,
            "aproveitamento_lance_livre": 89.0,
            "aproveitamento_bola_3": 39.5,
            "assistencias": 5,
            "rebotes_ofensivos": 2,
            "eficiencia": 32.8,
            "field_goal_percentage": 54.4,
            "toques_bola": 84,
            "minutos_jogados": 36.8
        },
        "defensiva": {
            "rebotes_defensivos": 7,
            "roubos_bola": 2,
            "bloqueios": 2,
            "turnovers": 3,
            "faltas": 2,
            "eficiencia": 30.1,
            "minutos_jogados": 36.8
        }
    },
    {
        "nome": "Jayson Tatum",
        "time": "Boston Celtics",
        "local_jogo": "casa",
        "ofensiva": {
            "pontos": 29,
            "bolas_3_convertidas": 4,
            "lances_livres_convertidos": 7,
            "aproveitamento_lance_livre": 85.4,
            "aproveitamento_bola_3": 38.2,
            "assistencias": 4,
            "rebotes_ofensivos": 3,
            "eficiencia": 31.7,
            "field_goal_percentage": 49.9,
            "toques_bola": 78,
            "minutos_jogados": 33.3
        },
        "defensiva": {
            "rebotes_defensivos": 7,
            "roubos_bola": 2,
            "bloqueios": 1,
            "turnovers": 2,
            "faltas": 2,
            "eficiencia": 29.2,
            "minutos_jogados": 33.3
        }
    },
    {
        "nome": "Joel Embiid",
        "time": "Philadelphia 76ers",
        "local_jogo": "fora",
        "ofensiva": {
            "pontos": 29,
            "bolas_3_convertidas": 1,
            "lances_livres_convertidos": 10,
            "aproveitamento_lance_livre": 82.1,
            "aproveitamento_bola_3": 31.4,
            "assistencias": 3,
            "rebotes_ofensivos": 4,
            "eficiencia": 34.3,
            "field_goal_percentage": 53.7,
            "toques_bola": 80,
            "minutos_jogados": 34.5
        },
        "defensiva": {
            "rebotes_defensivos": 10,
            "roubos_bola": 1,
            "bloqueios": 3,
            "turnovers": 3,
            "faltas": 3,
            "eficiencia": 31.0,
            "minutos_jogados": 34.5
        }
    },
    {
        "nome": "Luka Doncic",
        "time": "Dallas Mavericks",
        "local_jogo": "casa",
        "ofensiva": {
            "pontos": 31,
            "bolas_3_convertidas": 5,
            "lances_livres_convertidos": 8,
            "aproveitamento_lance_livre": 75.0,
            "aproveitamento_bola_3": 37.5,
            "assistencias": 8,
            "rebotes_ofensivos": 3,
            "eficiencia": 33.6,
            "field_goal_percentage": 47.8,
            "toques_bola": 90,
            "minutos_jogados": 35.0
        },
        "defensiva": {
            "rebotes_defensivos": 6,
            "roubos_bola": 2,
            "bloqueios": 1,
            "turnovers": 4,
            "faltas": 3,
            "eficiencia": 30.5,
            "minutos_jogados": 35.0
        }
    },
    {
        "nome": "Devin Booker",
        "time": "Phoenix Suns",
        "local_jogo": "fora",
        "ofensiva": {
            "pontos": 28,
            "bolas_3_convertidas": 5,
            "lances_livres_convertidos": 7,
            "aproveitamento_lance_livre": 87.3,
            "aproveitamento_bola_3": 39.8,
            "assistencias": 6,
            "rebotes_ofensivos": 2,
            "eficiencia": 29.9,
            "field_goal_percentage": 48.6,
            "toques_bola": 75,
            "minutos_jogados": 33.7
        },
        "defensiva": {
            "rebotes_defensivos": 4,
            "roubos_bola": 1,
            "bloqueios": 0,
            "turnovers": 2,
            "faltas": 2,
            "eficiencia": 27.1,
            "minutos_jogados": 33.7
        }
    },
    {
        "nome": "Anthony Edwards",
        "time": "Minnesota Timberwolves",
        "local_jogo": "casa",
        "ofensiva": {
            "pontos": 26,
            "bolas_3_convertidas": 3,
            "lances_livres_convertidos": 5,
            "aproveitamento_lance_livre": 79.0,
            "aproveitamento_bola_3": 36.5,
            "assistencias": 4,
            "rebotes_ofensivos": 3,
            "eficiencia": 29.8,
            "field_goal_percentage": 48.9,
            "toques_bola": 82,
            "minutos_jogados": 34.0
        },
        "defensiva": {
            "rebotes_defensivos": 6,
            "roubos_bola": 2,
            "bloqueios": 1,
            "turnovers": 3,
            "faltas": 2,
            "eficiencia": 28.0,
            "minutos_jogados": 34.0
        }
    }
]

# Inserir dados ofensivos e defensivos
ofensiva_docs = []
defensiva_docs = []
jogadores_docs = []
times_docs = []
partidas_docs = []
historico_docs = []

# Criar um conjunto de times únicos
times_unicos = {}
for jogador in jogadores:
    times_unicos[jogador["time"]] = {"nome": jogador["time"]}

# Inserir os times únicos na lista
for time in times_unicos.values():
    times_docs.append(time)

# Criar jogadores, ofensiva e defensiva a partir dos dados
for jogador in jogadores:
    # Jogador
    jogadores_docs.append({
        "nome": jogador["nome"],
        "time": jogador["time"],
        "local_jogo": jogador["local_jogo"]
    })

    # Ofensiva
    ofensiva_doc = {
        "nome": jogador["nome"],
        "time": jogador["time"],
        "local_jogo": jogador["local_jogo"],
        **jogador["ofensiva"]
    }
    ofensiva_docs.append(ofensiva_doc)

    # Defensiva
    defensiva_doc = {
        "nome": jogador["nome"],
        "time": jogador["time"],
        "local_jogo": jogador["local_jogo"],
        **jogador["defensiva"]
    }
    defensiva_docs.append(defensiva_doc)

# Criar partidas exemplo entre os times (relacionando os times inseridos)
partidas_docs = [
    {
        "time_casa": "Los Angeles Lakers",
        "time_fora": "Milwaukee Bucks",
        "data": "2025-02-15",
        "local": "Staples Center",
        "placar_casa": 112,
        "placar_fora": 110
    },
    {
        "time_casa": "Golden State Warriors",
        "time_fora": "Denver Nuggets",
        "data": "2025-02-16",
        "local": "Chase Center",
        "placar_casa": 120,
        "placar_fora": 115
    },
    {
        "time_casa": "Phoenix Suns",
        "time_fora": "Boston Celtics",
        "data": "2025-02-17",
        "local": "Footprint Center",
        "placar_casa": 118,
        "placar_fora": 121
    },
    {
        "time_casa": "Philadelphia 76ers",
        "time_fora": "Dallas Mavericks",
        "data": "2025-02-18",
        "local": "Wells Fargo Center",
        "placar_casa": 114,
        "placar_fora": 109
    },
    {
        "time_casa": "Minnesota Timberwolves",
        "time_fora": "Los Angeles Lakers",
        "data": "2025-02-19",
        "local": "Target Center",
        "placar_casa": 105,
        "placar_fora": 107
    }
]

# Histórico de jogador simples, por exemplo últimos 3 jogos (de forma resumida)
historico_docs = [
    {
        "nome": "LeBron James",
        "ultimos_jogos": [
            {"data": "2025-02-01", "pontos": 30, "assistencias": 10},
            {"data": "2025-02-05", "pontos": 25, "assistencias": 8},
            {"data": "2025-02-10", "pontos": 27, "assistencias": 9}
        ]
    },
    {
        "nome": "Giannis Antetokounmpo",
        "ultimos_jogos": [
            {"data": "2025-02-01", "pontos": 28, "assistencias": 6},
            {"data": "2025-02-05", "pontos": 32, "assistencias": 7},
            {"data": "2025-02-10", "pontos": 31, "assistencias": 8}
        ]
    },
    # ... você pode expandir para outros jogadores similarmente ...
    {
        "nome": "Anthony Edwards",
        "ultimos_jogos": [
            {"data": "2025-02-01", "pontos": 24, "assistencias": 5},
            {"data": "2025-02-05", "pontos": 26, "assistencias": 4},
            {"data": "2025-02-10", "pontos": 27, "assistencias": 6}
        ]
    }
]

# Função para limpar coleções (opcional para rodar do zero)
def limpar_colecoes():
    colecao_ofensiva.delete_many({})
    colecao_defensiva.delete_many({})
    colecao_jogadores.delete_many({})
    colecao_times.delete_many({})
    colecao_partidas.delete_many({})
    colecao_historico.delete_many({})

# Inserção dos documentos no banco
def inserir_tudo():
    limpar_colecoes()

    colecao_times.insert_many(times_docs)
    colecao_jogadores.insert_many(jogadores_docs)
    colecao_ofensiva.insert_many(ofensiva_docs)
    colecao_defensiva.insert_many(defensiva_docs)
    colecao_partidas.insert_many(partidas_docs)
    colecao_historico.insert_many(historico_docs)

    print("Inserção completa nas 6 coleções!")

if __name__ == "__main__":
    inserir_tudo()