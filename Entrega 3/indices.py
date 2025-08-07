from database import colecao_ofensiva

# Criação do índice sobre pontos
resultado = colecao_ofensiva.create_index([("estatisticas.pontos", -1)])

print(f"Índice criado: {resultado}")

# Verifica os índices existentes na coleção
indices = colecao_ofensiva.index_information()
for nome, info in indices.items():
    print(f"Índice: {nome} -> {info}")