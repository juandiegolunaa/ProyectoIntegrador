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
            # Preparar la solicitud en formato JSON (Sacado de documentación de Ollama)
            request_data = {
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }

            print(f"Enviando solicitud al modelo {model_name}...")

            # Empezar el contador de tiempo
            start_time = time.time()
            response = requests.post(server_address, headers={"Content-Type": "application/json"}, json=request_data, timeout=60)
            end_time = time.time()

            # Verificar si la respuesta fue exitosa
            if response.status_code == 200:
                response_json = response.json()
                # Obtener el eval_count (número de tokens) directamente del JSONz
                tokens = response_json.get("eval_count", 0)
                # Medir tiempo de respuesta
                response_time = end_time - start_time
                tokens_per_second = tokens / response_time if response_time > 0 else 0

                # Guardar todos los datos relevantes en el diccionario de resultados
                response_json["response_time"] = response_time
                response_json["tokens"] = tokens
                response_json["tokens_per_second"] = tokens_per_second
                response_json["model"] = model_name
                response_json["params"] = model_params.get(model_name, "Desconocido")

                # Guardar datos del JSON
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

# Realizar solicitudes para cada modelo en la lista
for model in models:
    response_data = request_generation(server_address, model, prompt)
    
    # Si se recibe una respuesta válida, guardarla en un archivo JSON
    if response_data:
        output_filename = f"ollama_response_{model.replace(':', '_')}.json"
        with open(output_filename, "w") as outfile:
            json.dump(response_data, outfile, indent=4)
        print(f"Respuesta guardada en '{output_filename}'.\n")

# Presentar los resultados en una tabla con todos los datos del JSON
df_results = pd.DataFrame(results)

# Mostrar la tabla directamente en la consola
print("\nTabla de resultados:")
print(df_results)

# Mostrar solo columnas específicas, incluyendo los parámetros
df_results = df_results[['model', 'params', 'response_time','tokens', 'tokens_per_second']]
# Mostrar la tabla ordenada
print("\nTabla de resultados ordenada:")
print(df_results)

