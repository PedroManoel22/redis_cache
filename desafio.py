import json
import os
import time
from typing import Any

import redis
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

_HOST = os.getenv("REDIS_HOST")
_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASS = os.getenv("REDIS_PASS")

if not _HOST or not _PORT:
    raise ValueError(
        "ERRO: REDIS_HOST e REDIS_PORT precisam estar definidos no arquivo .env"
    )

REDIS_HOST: str = _HOST
REDIS_PORT: int = int(_PORT)

app = Flask(__name__)


r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USER,
    password=REDIS_PASS,
)

# Simulação de um Banco de Dados de Produtos
# Em um cenário real, isso seria uma consulta a um DB ou serviço externo

DATABASE: dict[str, dict[str, Any]] = {
    "1": {
        "id": "1",
        "nome": "Smart TV 4K",
        "descricao": "TV de 55 polegadas com resolução 4K e HDR.",
        "preco": 3500.00,
    },
    "2": {
        "id": "2",
        "nome": "Fone de Ouvido Bluetooth",
        "descricao": "Cancelamento de ruído ativo e bateria de longa duração.",
        "preco": 800.00,
    },
    "3": {
        "id": "3",
        "nome": "Notebook Gamer",
        "descricao": "Processador de última geração e placa de vídeo dedicada.",
        "preco": 7000.00,
    },
}


def get_product_from_db(product_id: str):
    """Simula a busca de um produto no banco de dados com latência."""
    time.sleep(2)  # Simula uma operação lenta de 2 segundos
    return DATABASE.get(product_id)


def get_product_from_with_cache(product_id: str) -> dict[str, Any] | None:

    cache_key = f"product:{product_id}"
    cache_data = r.get(cache_key)

    if isinstance(cache_data, str):
        return json.loads(cache_data)

    print("Cache inexistente buscando no banco de dados")

    product_data = get_product_from_db(product_id)

    if product_data:
        print("Dados no banco de dados encontrada salvando no cache")
        r.set(cache_key, json.dumps(product_data))

    return product_data


@app.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id: str):
    product_data = get_product_from_with_cache(product_id)
    if not product_data:
        product_data = get_product_from_db(product_id)
    if product_data:
        return jsonify(product_data)
    return jsonify({"message": "Produto não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
