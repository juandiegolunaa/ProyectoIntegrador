from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from sentence_transformers import SentenceTransformer, util

# Modelo de embeddings para Answer Relevancy Metric
embedding_model = SentenceTransformer('all-mpnet-base-v2')
reference_answer = """DERECHOS, RESPONSABILIDADES Y OBLIGACIONES DE LOS ESTUDIANTES
El estudiante es el principal actor dentro de la comunidad
universitaria. Por ello, todo estudiante de la USFQ tiene derechos, responsabilidades y obligaciones que le ayudarán a
desarrollar su aprendizaje, en un ambiente de ética y honestidad en armonía con el resto de la comunidad USFQ.
Todo estudiante miembro de la comunidad USFQ tiene
derecho a:
1. Expresarse libremente, dentro de las limitaciones del
Código de Honor y Convivencia de la USFQ y de sus políticas.
2. Escoger una carrera para realizar sus metas académicas
siempre y cuando cumpla los requisitos y exigencias de
la carrera escogida.
3. Acceder alsyllabus de sus materias, ya sea por un medio
impreso o digital.
4. Hacer respetar la privacidad y confidencialidad de sus
expedientes estudiantiles de acuerdo con las políticas
de la USFQ
5. Ser evaluado justa y oportunamente por sus méritos
académicos y recibir una debida retroalimentación.
6. Conocer sus calificaciones, acceder a sus evaluaciones y
apelarlas de acuerdo con el proceso de Apelación de
Notas.
7. Revisar sus notas y avisar cualquier inconsistencia, inclusive si la nota recibida no fuera compatible con su
rendimiento y le estuviera dando una ventaja académica injusta.
8. Ejercer los derechos establecidos en la Ley Orgánica de
Educación Superior LOES.
Todo estudiante miembro de la comunidad USFQ tiene la
responsabilidad de:
1. Buscar la excelencia académica.
2. Asistir de manera regular y puntual a las clases y eventos propios de los estudios que realice.
3. Mantener el debido respeto, cordialidad y consideración con todos los miembros de la comunidad universitaria y conducirse de una manera íntegra en las áreas
académica, social y deportiva.
4. Cumplir con las tareas, trabajos, proyectos y cualquier
otra actividad académica que sus profesores demanden, con la mayor eficiencia y honestidad intelectual,
dentro de los plazos correspondientes.
5. Cumplir a cabalidad, dentro de la Universidad y en los
canales virtuales y redes sociales de la institución, así
como fuera de ella cuando la representan, las normas
de este manual, del Código de Honor y Convivencia y
demás normativa interna pertinente.
6. Respetar las demás normas que establezca la Ley Orgánica de Educación Superior LOES, su Reglamento y regulaciones afines expedidas por los organismos rectores del Sistema de Educación Superior.
7. Utilizar la cuenta de correo electrónico proporcionada
por la USFQ como la vía oficial y única de comunicación
con la Universidad, ya que toda la información enviada
por este medio se considerará como notificada.
Todo estudiante miembro de la comunidad USFQ tiene la
obligación de:
1. Mantener el promedio acumulado y de especialización
requerido por su carrera y colegio académico.
2. Cumplir con todos los requisitos académicos y administrativos de la carrera para la obtención del título universitario correspondiente.
3. Cumplir con sus obligaciones y acuerdos financieros
con la Universidad y otros requisitos administrativos."""
context_question = "Cuales son los DERECHOS, RESPONSABILIDADES Y OBLIGACIONES DE LOS ESTUDIANTES DE LA USFQ?"

#Answer Relevancy Metric
def calculate_relevancy_metric(generated_answer, reference_answer):
    gen_embedding = embedding_model.encode(generated_answer, convert_to_tensor=True)
    ref_embedding = embedding_model.encode(reference_answer, convert_to_tensor=True)
    relevancy_score = util.cos_sim(gen_embedding, ref_embedding).item()
    return relevancy_score

#Faithfulness con threshold 0.7
def calculate_faithfulness_metric(generated_answer, reference_answer, threshold=0.7):
    gen_embedding = embedding_model.encode(generated_answer, convert_to_tensor=True)
    ref_embedding = embedding_model.encode(reference_answer, convert_to_tensor=True)
    faithfulness_score = util.cos_sim(gen_embedding, ref_embedding).item()
    is_faithful = faithfulness_score > threshold  # Consideramos fiel si el puntaje es mayor al umbral
    return faithfulness_score, is_faithful

#Contextual Metric con threshold 0.7
def calculate_contextual_metric(generated_answer, context_question, threshold=0.7):
    gen_embedding = embedding_model.encode(generated_answer, convert_to_tensor=True)
    context_embedding = embedding_model.encode(context_question, convert_to_tensor=True)
    contextual_score = util.cos_sim(gen_embedding, context_embedding).item()
    is_contextual = contextual_score > threshold  # Consideramos contextual si el puntaje es mayor al umbral
    return contextual_score, is_contextual

#Monitorear texto generado
def monitor_text_generation(driver, user_id, max_wait_time=5, check_interval=0.5):
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
                print(f"Usuario {user_id}: El texto no ha cambiado en los últimos {max_wait_time} segundos.")
                return current_text  # Retorna el texto generado hasta el momento

        time.sleep(check_interval)

# Simulación de usuarios
def simulate_user_and_monitor(user_id):
    print(f"Iniciando usuario {user_id}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("http://172.21.230.10:3000/")
        time.sleep(10)

        # Credenciales
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su correo electrónico"]')
        email_input.send_keys(f"usuario{user_id}@gmail.com")

        password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Ingrese su contraseña"]')
        password_input.send_keys(f"usuario{user_id}")

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        try:
            # Selección de modelo
            menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Selecciona un modelo']"))
            )
            menu_button.click()

            model_search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "model-search-input"))
            )
            model_search_input.send_keys("llama3.1\n")

        except Exception as e:
            print(f"Error al interactuar con el menú de selección de modelo: {e}")
        
        # Enviar pregunta
        chat_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'chat-textarea')))
        chat_input.send_keys("Cuales son los DERECHOS, RESPONSABILIDADES Y OBLIGACIONES DE LOS ESTUDIANTES DE LA USFQ?")
        send_button = driver.find_element(By.ID, 'send-message-button')
        send_button.click()

        # Monitorear la generación de texto
        generated_text = monitor_text_generation(driver, user_id, max_wait_time=50, check_interval=0.5)

        # Calcular Answer Relevancy, Faithfulness y Contextual Metrics
        if generated_text:
            relevancy_score = calculate_relevancy_metric(generated_text, reference_answer)
            faithfulness_score, is_faithful = calculate_faithfulness_metric(generated_text, reference_answer)
            contextual_score, is_contextual = calculate_contextual_metric(generated_text, context_question)

            print(f"Usuario {user_id} completado:")
            print(f" - Relevancy Score = {relevancy_score:.4f}")
            print(f" - Faithfulness Score = {faithfulness_score:.4f}, Faithful: {is_faithful}")
            print(f" - Contextual Score = {contextual_score:.4f}, Contextual: {is_contextual}")

    except Exception as e:
        print(f"Usuario {user_id} tiene un error: {e}")

    finally:
        driver.quit()

# Para multiples usuarios
def simulate_multiple_users(num_users):
    threads = []
    for user_id in range(1, num_users + 1):
        thread = threading.Thread(target=simulate_user_and_monitor, args=(user_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Ejecutar la simulación para 5 usuarios simultáneos
simulate_multiple_users(5)
