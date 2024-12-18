import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import re

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

# Almacén de respuestas
responses = []

# Cargar preguntas del archivo JSON
def load_questions_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

questions = load_questions_from_json("preguntas_respuestas.json")

# Configurar el tamaño de la ventana del navegador
def configure_browser_window(driver, width=1920, height=1080):
    driver.set_window_size(width, height)
    print(f"Ventana configurada a {width}x{height}")

# Función para monitorear generación de texto
def monitor_text_generation(driver, max_wait_time=10, check_interval=0.5):
    text_container_selector = 'div.w-full.flex.flex-col'
    prev_text = ""
    start_time = time.time()

    while True:
        text_container = driver.find_element(By.CSS_SELECTOR, text_container_selector)
        current_text = text_container.text

        if current_text != prev_text:
            prev_text = current_text
            start_time = time.time()
        else:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_wait_time:
                return current_text

        time.sleep(check_interval)

# Limpiar la respuesta extraída
def clean_response(response_text, question_text):
    try:
        # Extraer desde la última pregunta hasta el mensaje final
        cleaned_response = re.search(
            re.escape(question_text) + r"(.*?)\n1\nmanual-del-estudiante-de-grado",
            response_text,
            re.DOTALL
        )
        if cleaned_response:
            return cleaned_response.group(1).strip()
        return ""
    except Exception as e:
        print(f"Error limpiando la respuesta: {e}")
        return ""

# Simular usuario para un modelo y mandar todas las preguntas
def simulate_user_for_model(user_id, model_name):
    print(f"Iniciando simulación para el usuario {user_id} con modelo {model_name}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        configure_browser_window(driver)
        driver.get("http://172.21.230.10:3000/")
        time.sleep(10)

        # Credenciales
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su correo electrónico"]')
        email_input.send_keys(f"usuario{user_id}@gmail.com")

        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su contraseña"]')
        password_input.send_keys(f"usuario{user_id}")

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

        # Selección de modelo
        menu_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Selecciona un modelo']"))
        )
        menu_button.click()

        model_search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-search-input"))
        )
        model_search_input.send_keys(model_name + "\n")

        # Enviar preguntas secuencialmente
        for question in questions:
            print(f"Usuario {user_id} enviando pregunta ID {question['id']} para el modelo {model_name}")
            chat_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'chat-textarea')))
            chat_input.send_keys("#\t",question["pregunta"])

            send_button = driver.find_element(By.ID, 'send-message-button')
            send_button.click()

            # Monitorear la generación de texto
            generated_text = monitor_text_generation(driver, max_wait_time=50, check_interval=0.5)

            # Limpiar la respuesta
            cleaned_text = clean_response(generated_text, question["pregunta"])

            # Guardar la respuesta
            if cleaned_text:
                responses.append({
                    "model": model_name,
                    "user_id": user_id,
                    "question_id": question["id"],
                    "response": cleaned_text
                })
                print(f"Usuario {user_id} con modelo {model_name} respondió a la pregunta ID {question['id']}: {cleaned_text}")

    except Exception as e:
        print(f"Error para el usuario {user_id} con modelo {model_name}: {e}")

    finally:
        driver.quit()

# Manejar el flujo principal
def simulate_models_and_save():
    for model in models:
        threads = []
        for user_id in range(1, 4):  # 5 usuarios en paralelo
            thread = threading.Thread(target=simulate_user_for_model, args=(user_id, model))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    # Guardar las respuestas en un archivo JSON
    with open("responses.json", "w", encoding="utf-8") as json_file:
        json.dump(responses, json_file, ensure_ascii=False, indent=4)

    print("\nRespuestas guardadas en responses.json")

# Ejecutar el script
simulate_models_and_save()
