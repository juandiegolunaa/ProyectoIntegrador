import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt

server_address = "http://172.21.230.10:11434/api/generate"

# Lista de modelos
models = [
    "llama3.2:3b",
    "phi3.5:latest",
    "llama2-uncensored:latest",
    "llama3.1:latest",
    "codegemma:latest",
    "gemma:latest",
    "gemma2:latest",
    "deepseek-coder-v2:16b",
    "llava:34b",
    "mixtral:latest",
    "llama3.1:70b"
]

# Diccionario con la cantidad de parámetros de cada modelo
model_params = {
    "llama3.2:3b": "3.2B",
    "phi3.5:latest": "3.8B",
    "llama2-uncensored:latest": "7B",
    "llama3.1:latest": "8B",
    "codegemma:latest": "9B",
    "gemma:latest": "9B",
    "gemma2:latest": "9.2B",
    "deepseek-coder-v2:16b": "15.7B",
    "llava:34b": "34B",
    "mixtral:latest": "47B",
    "llama3.1:70b": "70.6B"
}

# Prompt para realizar las pruebas
prompt = "Why is the sky blue?"
results = []

# Enviar requests y medir los tiempos
def request_generation(server_address, model_name, prompt):
    retries = 3
    for attempt in range(retries):
        try:
            request_data = {
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }

            print(f"Enviando solicitud al modelo {model_name}...")

            start_time = time.time()
            response = requests.post(server_address, headers={"Content-Type": "application/json"}, json=request_data, timeout=60)
            end_time = time.time()

            if response.status_code == 200:
                response_json = response.json()
                tokens = response_json.get("eval_count", 0)
                response_time = end_time - start_time
                tokens_per_second = tokens / response_time if response_time > 0 else 0

                response_json["response_time"] = response_time
                response_json["tokens"] = tokens
                response_json["tokens_per_second"] = tokens_per_second
                response_json["model"] = model_name
                response_json["params"] = model_params.get(model_name, "Desconocido")

                results.append(response_json)

                print(f"Modelo: {model_name} | Tiempo de respuesta: {response_time:.4f} segundos | Tokens: {tokens} | Parámetros: {model_params[model_name]}")

                return response_json
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None

        except (requests.Timeout, requests.ConnectionError, json.JSONDecodeError) as e:
            print(f"Error en el intento {attempt + 1}/{retries}: {e}")
            if attempt + 1 == retries:
                print("Todos los intentos fallaron.")
                return None

# Realizar solicitudes y calcular promedios
def gather_metrics(server_address, model_name, prompt, num_requests=20):
    response_times = []
    tokens_list = []
    tokens_per_second_list = []

    for i in range(num_requests):
        print(f"\n[{model_name}] Solicitud {i+1}/{num_requests}")
        response = request_generation(server_address, model_name, prompt)
        if response:
            response_times.append(response["response_time"])
            tokens_list.append(response["tokens"])
            tokens_per_second_list.append(response["tokens_per_second"])

    if response_times and tokens_list and tokens_per_second_list:
        avg_response_time = sum(response_times) / len(response_times)
        avg_tokens = sum(tokens_list) / len(tokens_list)
        avg_tokens_per_second = sum(tokens_per_second_list) / len(tokens_per_second_list)

        return {
            "model": model_name,
            "params": model_params.get(model_name, "Desconocido"),
            "avg_response_time": avg_response_time,
            "avg_tokens": avg_tokens,
            "avg_tokens_per_second": avg_tokens_per_second
        }
    else:
        return {
            "model": model_name,
            "params": model_params.get(model_name, "Desconocido"),
            "avg_response_time": None,
            "avg_tokens": None,
            "avg_tokens_per_second": None
        }

# Lista para guardar los promedios
averaged_results = []

# Realizar pruebas para cada modelo
for model in models:
    avg_metrics = gather_metrics(server_address, model, prompt)
    averaged_results.append(avg_metrics)

# Crear un DataFrame con los resultados promedio
df_avg_results = pd.DataFrame(averaged_results)

# Añadir columna con nombres de modelo y parámetros combinados
df_avg_results['model_with_params'] = df_avg_results.apply(lambda row: f"{row['model']} ({row['params']})", axis=1)

# Mostrar solo columnas relevantes
df_avg_results = df_avg_results[['model_with_params', 'avg_response_time', 'avg_tokens', 'avg_tokens_per_second']]

# Mostrar la tabla ordenada
print("\nTabla de resultados promedio:")
print(df_avg_results)

# Gráficos basados en promedios
# Gráfico 1: Tiempo de respuesta promedio por modelo
plt.figure(figsize=(10, 6))
plt.bar(df_avg_results['model_with_params'], df_avg_results['avg_response_time'], color='skyblue')
plt.title('Tiempo de Respuesta Promedio por Modelo')
plt.xlabel('Modelo (Parámetros)')
plt.ylabel('Tiempo de Respuesta Promedio (segundos)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Gráfico 2: Tokens promedio procesados por modelo
plt.figure(figsize=(10, 6))
plt.bar(df_avg_results['model_with_params'], df_avg_results['avg_tokens'], color='lightcoral')
plt.title('Tokens Promedio Procesados por Modelo')
plt.xlabel('Modelo (Parámetros)')
plt.ylabel('Tokens Promedio')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Gráfico 3: Tokens por segundo promedio por modelo
plt.figure(figsize=(10, 6))
plt.bar(df_avg_results['model_with_params'], df_avg_results['avg_tokens_per_second'], color='lightgreen')
plt.axhline(y=35.68, color='red', linestyle='--', label = "gpt-4-turbo-2024-04-09")
plt.title('Tokens por Segundo Promedio por Modelo')
plt.xlabel('Modelo (Parámetros)')
plt.ylabel('Tokens por Segundo Promedio')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
