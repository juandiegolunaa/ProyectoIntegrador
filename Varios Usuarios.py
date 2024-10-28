from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

# Función para monitorear si el texto generado por el chatbot se detiene
def monitor_text_generation(driver, user_id, max_wait_time=10, check_interval=0.5):

    text_container_selector = 'div.w-full.flex.flex-col'  # Selector del contenedor del texto generado
    prev_text = ""
    start_time = time.time()

    while True:
        # Obtener el texto actual generado por el chatbot
        text_container = driver.find_element(By.CSS_SELECTOR, text_container_selector)
        current_text = text_container.text

        # Verificar si el texto ha cambiado
        if current_text != prev_text:
            # Si el texto ha cambiado, reiniciar el temporizador
            prev_text = current_text
            start_time = time.time()
        else:
            # Si el texto no ha cambiado en `max_wait_time`, considerar que se detuvo
            elapsed_time = time.time() - start_time
            if elapsed_time > max_wait_time:
                print(f"Usuario {user_id}: El texto no ha cambiado en los últimos {max_wait_time} segundos.")
                return False

        # Esperar un tiempo antes de volver a verificar
        time.sleep(check_interval)

# Simulación de un usuario y monitoreo del chatbot
def simulate_user_and_monitor(user_id):
    print(f"Iniciando usuario {user_id}")

    # Configurar el servicio de ChromeDriver utilizando webdriver-manager
    service = Service(ChromeDriverManager().install())
    
    # Iniciar el navegador Chrome
    driver = webdriver.Chrome(service=service)

    try:
        # Abrir la página del chatbot
        driver.get("http://172.21.230.10:3000/")
        time.sleep(10)  # Espera que la página cargue completamente

        # Ingresar el correo electrónico
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su correo electrónico"]')
        email_input.send_keys(f"usuario{user_id}@gmail.com")  # Simular correos únicos por usuario

        # Ingresar la contraseña
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su contraseña"]')
        password_input.send_keys(f"usuario{user_id}")  # Contraseña compartida para todos

        # Hacer clic en el botón "Iniciar sesión"
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

        # Esperar hasta que aparezca la pantalla de bienvenida y el botón "Bien, ¡Vamos!"
        #welcome_button = WebDriverWait(driver, 20).until(
        #    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Bien, ¡Vamos!']]"))
        #)
        #welcome_button.click()

        # Localizar el campo de entrada del chatbot
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'chat-textarea'))
        )

        # Escribir la consulta en el campo de entrada
        chat_input.send_keys(f"Write 1000 words about AI")

        # Hacer clic en el botón de enviar
        send_button = driver.find_element(By.ID, 'send-message-button')
        send_button.click()

        # Monitorear el texto generado por el chatbot para ver si se detiene
        text_complete = monitor_text_generation(driver, user_id, max_wait_time=10, check_interval=0.5)

        if text_complete:
            print(f"Usuario {user_id} completado: El texto se generó completamente.")
        else:
            print(f"Usuario {user_id}: El texto se detuvo durante la generación.")

    except Exception as e:
        print(f"Usuario {user_id} encontró un error: {e}")

    finally:
        # Cerrar el navegador
        driver.quit()

# Simulación de múltiples usuarios
def simulate_multiple_users(num_users):
    threads = []

    # Crear e iniciar un hilo para cada usuario
    for user_id in range(1, num_users + 1):
        thread = threading.Thread(target=simulate_user_and_monitor, args=(user_id,))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

# Ejecutar la simulación para 10 usuarios simultáneos
simulate_multiple_users(10)
