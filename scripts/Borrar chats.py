from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Función para borrar el chat
def delete_chat(driver):
    try:
        # 1. Encontrar el contenedor del chat donde queremos pasar el mouse
        chat_container = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.w-full.pr-2.relative.group'))
        )
        
        # 2. Simular el hover sobre el chat para que aparezca el botón "Más"
        actions = ActionChains(driver)
        actions.move_to_element(chat_container).perform()
        time.sleep(1)  # Añadir un pequeño retraso para que el botón "Más" sea visible

        # 3. Hacer clic en el botón "Más"
        more_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Chat Menu"]'))
        )
        more_button.click()
        
        # 4. Hacer clic en la opción "Borrar"
        delete_option = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Borrar')]"))
        )
        delete_option.click()

        # 5. Confirmar la eliminación
        confirm_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirmar')]"))
        )
        confirm_button.click()

        print("Chat eliminado con éxito.")
    except Exception as e:
        print(f"Error al eliminar el chat: {e}")

# Función para ingresar al sistema y eliminar el chat 100 veces
def login_and_delete_chats():
    # Configurar el servicio de ChromeDriver utilizando webdriver-manager
    service = Service(ChromeDriverManager().install())

    # Iniciar el navegador Chrome
    driver = webdriver.Chrome(service=service)

    try:
        # Abrir la página del chatbot
        driver.get("http://172.21.230.10:3000/")
        time.sleep(2)  # Espera que la página cargue completamente

        # Ingresar el correo electrónico
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su correo electrónico"]')
        email_input.send_keys("juan2002luna@gmail.com")

        # Ingresar la contraseña
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su contraseña"]')
        password_input.send_keys("Nosequeponerxd02?")

        # Hacer clic en el botón "Iniciar sesión"
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Esperar hasta que aparezca la pantalla de bienvenida y el botón "Bien, ¡Vamos!"
        welcome_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Bien, ¡Vamos!']]"))
        )
        welcome_button.click()

        # Esperar hasta que cargue el chat
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.w-full.pr-2.relative.group'))
        )
        
        # Repetir el proceso de borrar el chat
        for i in range(100):
            print(f"Eliminando chat {i+1} de 100...")
            delete_chat(driver)
            time.sleep(2)  # Añadir un pequeño retraso entre cada eliminación
    except Exception as e:
        print(f"Error durante el proceso: {e}")
    finally:
        # Cerrar el navegador
        driver.quit()

# Ejecutar la función para ingresar y eliminar chats
login_and_delete_chats()
