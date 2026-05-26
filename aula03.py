import json
import time
from typing import Any

import redis

# Atualizando e Sicronizando Dados no Cache

REDIS_HOST = "street-macrosleek-debt-10830.db.redis.io"
REDIS_PORT = 12096
REDIS_USER = "default"
REDIS_PASS = "kDNXskec3eXyFSU4PfOyEKRVDl7X5iLr"

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    username=REDIS_USER,
    password=REDIS_PASS,
)

DATABASE: dict[str, dict[str, Any]] = {
    "prod1": {"id": 1, "nome": "notebook Positivo", "valor": 159.56},
    "prod2": {"id": 2, "nome": "notebook Dell", "valor": 256.56},
    "prod3": {"id": 3, "nome": "notebook HP", "valor": 365.56},
}


def get_product_from_db(product_id: str) -> dict[str, Any] | None:
    print(f"[consulta] Consultando produto {product_id} no banco de dados...")
    time.sleep(5)
    return DATABASE.get(product_id)


def get_product_from_db_with_cache(product_id: str) -> dict[str, Any] | None:
    print(f"[consulta] Consultando produto {product_id} no banco de dados com cache...")

    cache_key = f"product:{product_id}"
    cache_data = r.get(cache_key)

    if isinstance(cache_data, str):
        print(
            f"[consulta no cache] produto {product_id} existia no cache retornando ao usuário..."
        )
        return json.loads(cache_data)

    print("Cache inexistente buscando no banco de dados")

    product_data = get_product_from_db(product_id)

    if product_data:
        print("Dados no banco de dados encontrada salvando no cache")
        r.set(cache_key, json.dumps(product_data))

    return product_data


def update_product_by_id(product_id: str, new_price: float):
    print(f"Atualizando produto {product_id} para o novo preço {new_price}")
    time.sleep(0.5)

    if product_id in DATABASE:
        DATABASE[product_id]["valor"] = new_price

        cache_key = f"product:{product_id}"
        r.delete(cache_key)
        print("Deletando do cache")
        return True

    return False


print("--- SIMULADOR DE CACHE ---")
produto_id = input("Digite o Id do produto que deseja consultar: ")


# Usando cache
product_data = get_product_from_db_with_cache(produto_id)
print("Informações obtidas")
print(product_data)

print("Simulando um Update")
update_ok = update_product_by_id(produto_id, 550.56)

product_data = get_product_from_db_with_cache(produto_id)
print("Informações obtidas após o update")
print(product_data)
