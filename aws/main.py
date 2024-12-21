import time
import datetime
import os
import random

import pandas as pd

#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#Modificar opciones de webdriver Chrome
from selenium.webdriver.chrome.options import Options
# Definir tipo de busqueda
from selenium.webdriver.common.by import By
# Manejar opciones de Select
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from tempfile import mkdtemp

# Configuración General

URL = 'https://scw.pjn.gov.ar/scw/home.seam'

# Variables 
select_jurid = '10'
jurisdi = 'COM - Camara Nacional de Apelaciones en lo comercial' 
tex_parte = 'RESIDUOS'

# Identificadores ID
ID_FORM_PUBLICA = 'formPublica:porParte:header:inactive'
ID_JURIDICCION = 'formPublica:camaraPartes'
ID_PARTE = 'formPublica:nomIntervParte'
ID_BUSCAR = 'formPublica:buscarPorParteButton'
ID_EXPEDIENTE_JURI = 'expediente:j_idt90:detailCamera'
ID_EXPEDIENTE_DEPE = 'expediente:j_idt90:detailDependencia'
ID_EXPEDIENTE_SITU = 'expediente:j_idt90:detailSituation'
ID_EXPEDIENTE_CARA = 'expediente:j_idt90:detailCover'
ID_INTERVINIENTES = 'expediente:j_idt261:header:inactive'

# XPATH
XP_RECAPCHA = '//*[@id="recaptcha-anchor"]/div[1]'
XP_DATATABLE = '//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr'
XP_DATATABLE_COLUM = '//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr[1]/td'
XP_EXPEDIENTE = '//*[@id="expediente:j_idt90:j_idt91"]/div/div[1]/div/div/div[2]/span'
XP_PAGINACION_TEXTO_SIG = '//*[@id="expediente:j_idt208:divPagesAct"]/ul/li[contains(@class,"active")]/span/following::a[1]/span'
XP_PAGINACION_BTN_SIG = '//*[@id="expediente:j_idt208:divPagesAct"]/ul/li[contains(@class,"active")]/span/following::a[1]'
XP_PARTICIPANTES = '//*[@id="expediente:participantsTable"]/tbody[contains(@class,"rf-dt-b")]'
XP_RECAPCHA_ = '//*[@id="recaptcha-anchor"]'
XP_ACTUACIONES_FILAS = '//*[@id="expediente:action-table"]/tbody/tr'
XP_ACTUACIONES_COLUM = '//*[@id="expediente:action-table"]/tbody/tr[1]/td'


# Funciones Auxiliares
def clear():
    """
        Limpiar la terminal al iniciar el script
    """

    if os.name == "posix":
        os.system ("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system ("cls")


def start_chrome():
    """
    Start chrome with the established configuration and return the driver.

    Returns:
        driver (webdriver.WebDriver): Objeto WebDriver que representa el navegador web.    
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    #Instanciar servicio de chrome
    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    return driver


def recapcha(driver):
    """
    Verifica si el reCAPTCHA fue resuelto satisfactoriamente con manejo de errores y tiempos de espera.

    Args:
        driver (webdriver.WebDriver): Objeto WebDriver que representa el navegador web.

    Returns:
        bool: True si el reCAPTCHA se resolvió correctamente, False en caso contrario.

    Esta función espera a que el atributo "aria-checked" del elemento reCAPTCHA cambie a "true", indicando que el desafío ha sido completado. 

    **Nota:** Esta función asume que el reCAPTCHA se resolverá de forma automática o manual.
    Para una solución más robusta, se podría implementar un mecanismo de resolución automática utilizando servicios especializados.
    """
    
    captcha = driver.find_element(By.XPATH, XP_RECAPCHA_)
    value = captcha.get_attribute("aria-checked")
    n = 0
    while value == 'false':
        time.sleep(0.5)
        captcha = driver.find_element(By.XPATH, XP_RECAPCHA_)
        value = captcha.get_attribute("aria-checked")
        n += 1

        if n == 60:
            return False
        
    return True

    
def get_information(driver):
    """
    Extrae información relevante de un expediente desde el navegador web controlado por el drlambdaiver.

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
    
    time.sleep(3)
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
        time.sleep(3)
        # # Identificar filas y columnas de la tabla por página
        rows = driver.find_elements(By.XPATH, XP_ACTUACIONES_FILAS)
        columns = driver.find_elements(By.XPATH, XP_ACTUACIONES_COLUM)

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

            # print(f'pagina: {pag}')

            if pag != 'Ver históricas': # Si no es la última página
                # Hacer clic en el botón "Siguiente"
                driver.find_element(By.XPATH, XP_PAGINACION_BTN_SIG).click()
                time.sleep(3)

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

    time.sleep(5)

    # Obtener Partes
    rows_parte = driver.find_elements(By.XPATH, XP_PARTICIPANTES)
    
    intervinientes = []
    if len(rows_parte) > 0:

        for i in range(len(rows_parte)):
 
            parte_fila = {
            'tipo' :driver.find_element(By.XPATH, f'//*[@id="expediente:participantsTable"]/tbody[contains(@id,"expediente:participantsTable:{i}:tb")]/tr/td[1]/span[2]').text,

            'nombre' : driver.find_element(By.XPATH, f'//*[@id="expediente:participantsTable"]/tbody[contains(@id,"expediente:participantsTable:{i}:tb")]/tr/td[2]/span[2]').text
            }

            intervinientes.append(parte_fila)

    return intervinientes 

def list_to_table(list):
    """
    Combierte datos en tabla y genera un archivo .csv

    Args:
        list: Una lista de diccionarios, donde cada diccionario representa los datos recopilados de cada expediente. Cada diccionario contiene:
            * expediente_numero: Número del expediente.
            * jurisdicción: Jurisdicción del expediente.
            * dependencia: Dependencia encargada del expediente.
            * situacion_actual: Situación actual del expediente.
            * caratula: Carátula del expediente.
            * actuaciones: Lista de actuaciones relacionadas con el expediente (obtenida de la función get_table_actuaciones).
            * intervinientes: Lista de intervinientes en el expediente (obtenida de la función get_intervinientes).


    Returns:
        bool: True si el archivo 'expedientes_qanlex.csv' se ha generado correctamente, False en caso contrario.

    Esta función utiliza toda la información recabada en el proceso de scarping y crea un archivo .csv para la realización de análisis posteriormente.
    """
    try:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M"))
        df = pd.DataFrame(list) 
        df.to_csv(f'data/raw/expedientes_qanlex_{date}.csv', sep=',', index=False, encoding='utf-8')
        print('Archivo "expedientes_qanlex.csv" generado correctamente')
        print('ubicado en: scraper/data/raw')
        return True
    
    except OSError as e:
        print ( f'Error ocurrido al crear archivo csv: {e} ' )
        df.to_csv('expedientes_qanlex.csv', sep=',', index=False, encoding='utf-8')
        return True
    
    except Exception as e:
        print ( f'Error ocurrido al crear archivo csv: {e} ' )
               
    return False

def lambda_scraping():
    try:
    
        inicio = time.time()
        clear()
        print('  INICIO DE SCRAPING  '.center(80, '-'))
        print('-'*80)

        driver = start_chrome()  # Se crea instancia de webdriver.Chrome con options predefinidas
        wait = WebDriverWait(driver, 50)

        driver.get(URL)

        carga_pagina = time.time()

        print('Ingresando a pagina solicitada ......')
        # Ingresar a pagina de Consulta pública por Parte
        driver.find_element(By.ID, ID_FORM_PUBLICA).click()

        print('Rellenando información de busqueda ......')
        # Rellenar información de busqueda
        wait.until(ec.visibility_of_element_located((By.ID, ID_JURIDICCION)))

        # Jurisdiccion
        jurisdiccion = Select(driver.find_element(By.ID, ID_JURIDICCION))
        jurisdiccion.select_by_value(select_jurid)
        # Parte
        parte = driver.find_element(By.ID, ID_PARTE)
        parte.send_keys(tex_parte)
        # Boton
        button = driver.find_element(By.ID, ID_BUSCAR)

        time.sleep(random.uniform(1.3,4))
        
        rellenar_información = time.time()

        print('Solucionando reCAPCHA ......')
        # Seleccionar reCAPCHA
        driver.switch_to.frame(0)
        driver.find_element(By.XPATH, XP_RECAPCHA).click()

        if not recapcha(driver):
            raise ValueError("Tiempo de resolución de reCAPCHA exedido")

        print('reCAPCHA Resuelto ......')

        driver.switch_to.default_content()
        button.click()

        resolver_recapcha = time.time()

        print('Entrando a pagina de consulta ......')

        # Trabajar con Tabla
        # Identificar Filas de tabla
        time.sleep(3)
        rows = driver.find_elements(By.XPATH, XP_DATATABLE)
        columns = driver.find_elements(By.XPATH, XP_DATATABLE_COLUM)

        expedientes = []

        btt_pag = 'Siguiente'

        while btt_pag == 'Siguiente':

            for i in range(1, len(rows)+1):

                wait.until(ec.element_to_be_clickable((By.XPATH, f'//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr[{i}]/td[6]/div/a')))
                time.sleep(3)
                
                driver.find_element(By.XPATH, f'//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr[{i}]/td/div').click()


                # Extraer información
                expediente = get_information(driver)
                expedientes.append(expediente)


                print(f'  Expediente # {expediente["expediente_numero"]} extraído '.center(80, '-'))
                
                driver.back()

            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'ul.pagination')))
            btt_pag = driver.find_element(By.CSS_SELECTOR, 'ul.pagination').text

            print(btt_pag)
            
            if btt_pag == 'Siguiente':
                driver.find_element(By.CSS_SELECTOR, 'ul.pagination').click()
                time.sleep(3)
                
        # file = list_to_table(expedientes)

        final =time.time()
        print()
        print('-'*80)
        print('Analisis tiempo de procesamiento script')
        print('-'*80)
        print(f'Tiempo Carga de página .................................... {carga_pagina - inicio}')
        print(f'Tiempo rellenar información ............................... {rellenar_información - carga_pagina}')
        print(f'Tiempo resolver recapcha .................................. {resolver_recapcha - rellenar_información}')
        print(f'Tiempo recolectar datos ................................... {final - resolver_recapcha}')
        print('-'*80)
        print(f'Tiempo Total de procesamiento: {final - inicio} segundos')
        print('-'*80)
        print('Información General de los datos recabados:')
        print('-'*80)
        print(f'Cantidad de registros ..................................... {len(expedientes)}')
        print(f'Jurisdición analisada ..................................... {jurisdi}')
        print(f'Parte analisada ........................................... {tex_parte}')
        print('-'*80)

        return expedientes
    
    except ValueError as e: 
        # Manejar otros errores de análisis 
        print ( f'Error ocurrido : {e} ' ) 
        driver.quit()
    except Exception as e: 
        # Manejar otros errores de análisis 
        print ( f'Error ocurrido al analizar HTML: {e} ' ) 
        driver.quit()
    finally : 
        # Cerrar la instancia de webdriver
        driver.quit()