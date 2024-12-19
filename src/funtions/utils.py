import time
import os

# Automatiza instalación de chorme driver
from webdriver_manager.chrome import ChromeDriverManager

#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#Modificar opciones de webdriver Chrome
from selenium.webdriver.chrome.options import Options
# Definir tipo de busqueda
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from funtions.config import XP_EXPEDIENTE, ID_EXPEDIENTE_JURI, ID_EXPEDIENTE_DEPE, ID_EXPEDIENTE_SITU, ID_EXPEDIENTE_CARA, XP_PAGINACION_TEXTO_SIG, XP_PAGINACION_BTN_SIG, ID_INTERVINIENTES, XP_PARTICIPANTES, XP_RECAPCHA_, XP_ACTUACIONES_FILAS, XP_ACTUACIONES_COLUM



def clear():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system ("cls")


def start_chrome():
    """
        Start chrome with the established configuration and return the driver.
    """

    # instalación de chromedriver correspondiente
    ruta = ChromeDriverManager().install()

    #Opciones de chrome
    options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--no-first-run')
    options.add_argument('--no-proxy-server')
    options.add_argument('--disable-blink-features=AutomationControlled')

    #Parametros a Omitir
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]
    options.add_experimental_option('excludeSwitches', exp_opt)

    #Preferencias en Chromedriver
    prefs = {
        'profile.default_content_setting_values.notifications' : 2,
        'intl.accept_languages' : ['es-ES', 'es'],
        'credentials_enable_service' : False
    }
    options.add_experimental_option('prefs', prefs)

    #Instanciar servicio de chrome
    ser = Service(ruta)
    driver = webdriver.Chrome(service=ser, options=options)

    return driver


def recapcha(driver):
    """
    Verifica si el reCAPTCHA fue resuelto satisfactoriamente con manejo de errores y tiempos de espera.

    Args:
        driver (webdriver.WebDriver): Objeto WebDriver que representa el navegador web.

    Returns:
        bool: True si el reCAPTCHA se resolvió correctamente, False en caso contrario.
    """
    
    try:
        captcha = driver.find_element(By.XPATH, XP_RECAPCHA_)
        value = captcha.get_attribute("aria-checked")
        
        while value == 'false':
            time.sleep(0.5)
            captcha = driver.find_element(By.XPATH, XP_RECAPCHA_)
            value = captcha.get_attribute("aria-checked")

        return True

    except NoSuchElementException:
        print("No se encontró el elemento del reCAPTCHA.")
    except TimeoutException:
        print("Se excedió el tiempo de espera.")
    except:
        print("Ha ocurrido un error.")

    return False


def get_information(driver):
    """
    Extrae información relevante de un expediente desde el navegador web controlado por el driver.

    Args:
        driver (webdriver.WebDriver): Objeto WebDriver que representa el navegador web.

    Returns:
        dict: Un diccionario que contiene los datos extraídos del expediente, incluyendo:
            * expediente_numero: Número del expediente.
            * jurisdicción: Jurisdicción del expediente.
            * dependencia: Dependencia encargada del expediente.
            * situacion_actual: Situación actual del expediente.
            * caratula: Carátula del expediente.
            * actuaciones: Lista de actuaciones relacionadas con el expediente (obtenida de la función get_table_actuaciones).
            * intervinientes: Lista de intervinientes en el expediente (obtenida de la función get_intervinientes).

    Esta función busca los elementos HTML correspondientes a cada dato del expediente utilizando los identificadores proporcionados y extrae su texto.
    Los datos de actuaciones e intervinientes se obtienen llamando a las funciones get_table_actuaciones y get_intervinientes, respectivamente.
    """
    
    expediente = {
        # Extracción de Información Relevante
        'expediente_numero' : driver.find_element(By.XPATH, XP_EXPEDIENTE).text,
        'jurisdicción' : driver.find_element(By.ID, ID_EXPEDIENTE_JURI).text,
        'dependencia' : driver.find_element(By.ID, ID_EXPEDIENTE_DEPE).text,
        'situacion_actual': driver.find_element(By.ID, ID_EXPEDIENTE_SITU).text,
        'caratula' : driver.find_element(By.ID, ID_EXPEDIENTE_CARA).text,
        'actuaciones' : get_table_actuaciones(driver),
        'intervinientes' : get_intervinientes(driver)

    }

    return expediente

def get_table_actuaciones(driver):
    """
    Extrae información de las actuaciones de un expediente desde el navegador web controlado por el driver.

    Args:
        driver (webdriver.WebDriver): Objeto WebDriver que representa el navegador web.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa una actuación del expediente. Cada diccionario contiene:
            * oficina: Oficina que realizó la actuación.
            * fecha: Fecha de la actuación.
            * tipo: Tipo de actuación.
            * descripcion: Descripción de la actuación.

    Esta función itera a través de las páginas de la tabla de actuaciones del expediente y extrae la información de cada fila. La paginación se maneja hasta que se encuentre el texto "Ver históricas" o no se encuentren más filas.
    """

    pag = 1
    actuaciones = []  # Lista para almacenar las actuaciones
    while pag != 'Ver históricas':

        # # Identificar filas y columnas de la tabla por página
        rows = driver.find_elements(By.XPATH, XP_ACTUACIONES_FILAS)
        columns = driver.find_elements(By.XPATH, XP_ACTUACIONES_COLUM)

        print(f'{len(rows)} | {len(columns)}')

        if len(rows) > 0:  # Si hay filas en la tabla
        
            for i in range(1, len(rows)+1):
                # Extraer información de cada fila            
                actuaciones_fila = {
                'oficina' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table:{i-1}:officeColumn"]').text,
                'fecha' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table"]/tbody/tr[{i}]/td[3]/span[2]').text,
                'tipo' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table"]/tbody/tr[{i}]/td[4]/span[2]').text,
                'descripcion' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table"]/tbody/tr[{i}]/td[5]/span[2]').text
                }
                actuaciones.append(actuaciones_fila)

            # Verificar texto de paginación
            pag = driver.find_element(By.XPATH, XP_PAGINACION_TEXTO_SIG).text

            print(f'pagina: {pag}')

            if pag != 'Ver históricas': # Si no es la última página
                # Hacer clic en el botón "Siguiente"
                driver.find_element(By.XPATH, XP_PAGINACION_BTN_SIG).click()
                time.sleep(5)

        else:
            break  # Si no hay filas, salir del ciclo
    
    return actuaciones


def get_intervinientes(driver):
    """
    Extrae información de los intervinientes de un expediente desde el navegador web controlado por el driver.

    Args:
        driver (webdriver.WebDriver): Objeto WebDriver que representa el navegador web.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un interviniente del expediente. Cada diccionario contiene:
            * tipo: Tipo de interviniente (por ejemplo, Demandante, Demandado).
            * nombre: Nombre del interviniente.

    Esta función simula una interacción con la página para acceder a la sección de intervinientes del expediente y luego extrae la información de cada fila de la tabla correspondiente.
    """
    

    # Ingresar a pagina de Consulta pública por Parte
    driver.find_element(By.ID, ID_INTERVINIENTES).click()

    time.sleep(3)

    # Obtener Partes
    rows_parte = driver.find_elements(By.XPATH, XP_PARTICIPANTES)
    
    intervinientes = []
    if len(rows_parte) > 0:

        for i in range(len(rows_parte)):
            
            print(f'fila partes N° {i}')

            parte_fila = {
            'tipo' :driver.find_element(By.XPATH, f'//*[@id="expediente:participantsTable"]/tbody[contains(@id,"expediente:participantsTable:{i}:tb")]/tr/td[1]/span[2]').text,

            'nombre' : driver.find_element(By.XPATH, f'//*[@id="expediente:participantsTable"]/tbody[contains(@id,"expediente:participantsTable:{i}:tb")]/tr/td[2]/span[2]').text
            }

            intervinientes.append(parte_fila)

    return intervinientes    