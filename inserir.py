from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongouri = os.getenv("host")

if not mongouri:
    raise ValueError("A variável 'host' não foi encontrada no arquivo .env")

client = MongoClient(mongouri)
db = client["desempenhoJogadoresNBA"]

colecao_ofensiva = db["ofensiva"]
colecao_defensiva = db["defensiva"]

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
    }
]

try:
    ofensiva_docs = [{k: jogador[k] for k in ("nome", "time", "local_jogo")} | jogador["ofensiva"] for jogador in jogadores]
    defensiva_docs = [{k: jogador[k] for k in ("nome", "time", "local_jogo")} | jogador["defensiva"] for jogador in jogadores]

    result_ofensiva = colecao_ofensiva.insert_many(ofensiva_docs)
    result_defensiva = colecao_defensiva.insert_many(defensiva_docs)

    print("Documentos inseridos na coleção ofensiva:")
    for _id in result_ofensiva.inserted_ids:
        print(f"  - {_id}")

    print("\nDocumentos inseridos na coleção defensiva:")
    for _id in result_defensiva.inserted_ids:
        print(f"  - {_id}")

except Exception as e:
    print("Erro ao inserir documentos:", e)