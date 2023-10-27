import requests

# Definir la URL base de la API
base_url = "http://localhost:8881/v1"

# Caso 1: No-Comprador 3 obtiene los detalles del ItemId=1
response = requests.get(f"{base_url}/query?item_id=1")
data = response.json()
print("Punto 1 - Detalles del ItemId=1 para No-Comprador 3:")
print(data)

# Caso 2: Comprador 1 hace la compra
payload_comprador1 = {
    "id": 1,
    "quantity": 1,
    "version": 1
}
response = requests.post(f"{base_url}/buy", json=payload_comprador1)
print("Punto 2 - Comprador 1 realiza la compra:")
print(response.text)

# Caso 3: Comprador 2 hace la compra
payload_comprador2 = {
    "id": 1,
    "quantity": 1,
    "version": 1
}
response = requests.post(f"{base_url}/buy", json=payload_comprador2)
print("Punto 3 - Comprador 2 realiza la compra:")
print(response.text)

# Caso 4: No-Comprador 3 obtiene los detalles del ItemId=1 nuevamente
response = requests.get(f"{base_url}/query?item_id=1")
data = response.json()
print("Punto 4 - Detalles del ItemId=1 para No-Comprador 3 después de las compras:")
print(data)
