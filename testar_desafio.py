import requests

BASE_URL = "http://127.0.0.1:5000/products/"


def main():
    print("=== Teste da API Flask ===")
    while True:
        product_id = input(
            "\nDigite o ID do produto (1, 2, 3) ou 'sair' para encerrar: "
        )

        if product_id.lower() == "sair":
            print("Encerrando teste da API...")
            break

        try:
            response = requests.get(BASE_URL + product_id)
            if response.status_code == 200:
                product = response.json()
                print("\n✅ Produto encontrado:")
                print(f"ID: {product['id']}")
                print(f"Nome: {product['nome']}")
                print(f"Descrição: {product['descricao']}")
                print(f"Preço: R$ {product['preco']:.2f}")
            else:
                print("⚠️ Produto não encontrado!")
        except requests.exceptions.RequestException as e:
            print("❌ Erro ao conectar com a API:", e)


if __name__ == "__main__":
    main()
