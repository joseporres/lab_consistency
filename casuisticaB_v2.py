import requests
import concurrent.futures

# Función para obtener los detalles del ItemId=1
def get_item_details():
    response = requests.get("http://localhost:8881/v1/query?item_id=1")
    data = response.json()
    return data

# Función para que un comprador realice la compra
def comprar_comprador(comprador_id):
    payload = {
        "id": comprador_id,
        "quantity": 20,
        "version": 1
    }
    response = requests.post("http://localhost:8881/v1/buy-transaction", json=payload)
    return response.text

# Realizar las solicitudes en paralelo
resultado_caso1 = get_item_details()
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Caso 1: No-Comprador 3 obtiene los detalles del ItemId=1

    # Caso 2: Comprador 1 y Comprador 2 hacen la compra en paralelo
    resultado_comprador1 = executor.submit(comprar_comprador, 1)
    resultado_comprador2 = executor.submit(comprar_comprador, 1)

    # Esperar a que se completen las compras
    comprador1_response = resultado_comprador1.result()
    comprador2_response = resultado_comprador2.result()

    # Caso 3: No-Comprador 3 obtiene los detalles del ItemId=1 nuevamente
resultado_caso3 = get_item_details()

# Imprimir resultados
print("Punto 1 - Detalles del ItemId=1 para No-Comprador 3:")
print(resultado_caso1)

print("Punto 2 - Comprador 1 realiza la compra:")
print(comprador1_response)

print("Punto 2 - Comprador 2 realiza la compra:")
print(comprador2_response)

print("Punto 3 - Detalles del ItemId=1 para No-Comprador 3 después de las compras:")
print(resultado_caso3)
