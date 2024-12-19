import time
import random

# Automatiza instalación de chorme driver
from webdriver_manager.chrome import ChromeDriverManager

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
from selenium.common.exceptions import TimeoutException


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
        Documentar
    """
    
    captcha = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
    value = captcha.get_attribute("aria-checked")
    # print(f'valor de atributo "aria-checked" Inicial: {value}')

    while value == 'false':
        time.sleep(0.5)
        captcha = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
        value = captcha.get_attribute("aria-checked")
        # print(f'valor de atributo "aria-checked" Inicial: {value}')

    return True

def get_information(driver):
    """
        Documentar
    """
    
    expediente = {
        # Extracción de Información Relevante
        'expediente_numero' : driver.find_element(By.XPATH, '//*[@id="expediente:j_idt90:j_idt91"]/div/div[1]/div/div/div[2]/span').text,
        'jurisdicción' : driver.find_element(By.ID, 'expediente:j_idt90:detailCamera').text,
        'dependencia' : driver.find_element(By.ID, 'expediente:j_idt90:detailDependencia').text,
        'situacion_ actual': driver.find_element(By.ID, 'expediente:j_idt90:detailSituation').text,
        'caratula' : driver.find_element(By.ID, 'expediente:j_idt90:detailCover').text,
        'actuaciones' : get_table_actuaciones(driver),
        'intervinientes' : get_intervinientes(driver)

    }

    return expediente

def get_table_actuaciones(driver):

    pag = 1
    actuaciones = []
    while pag != 'Ver históricas':

        # Identificar Filas de tabla
        rows = driver.find_elements(By.XPATH, '//*[@id="expediente:action-table"]/tbody/tr')
        columns = driver.find_elements(By.XPATH, '//*[@id="expediente:action-table"]/tbody/tr[1]/td')

        print(f'{len(rows)} | {len(columns)}')

        if len(rows) > 0:
        
            for i in range(1, len(rows)+1):
                            
                actuaciones_fila = {
                'oficina' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table:{i-1}:officeColumn"]').text,
                'fecha' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table"]/tbody/tr[{i}]/td[3]/span[2]').text,
                'tipo' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table"]/tbody/tr[{i}]/td[4]/span[2]').text,
                'descripcion' : driver.find_element(By.XPATH, f'//*[@id="expediente:action-table"]/tbody/tr[{i}]/td[5]/span[2]').text
                }
                actuaciones.append(actuaciones_fila)

            pag = driver.find_element(By.XPATH, '//*[@id="expediente:j_idt208:divPagesAct"]/ul/li[contains(@class,"active")]/span/following::a[1]/span').text

            print(f'pagina: {pag}')

            if pag != 'Ver históricas':
                driver.find_element(By.XPATH, '//*[@id="expediente:j_idt208:divPagesAct"]/ul/li[contains(@class,"active")]/span/following::a[1]').click()

        else:
            break
    
    return actuaciones

def get_intervinientes(driver):

    # expediente:j_idt261:header:active

    # Ingresar a pagina de Consulta pública por Parte
    driver.find_element(By.ID, 'expediente:j_idt261:header:inactive').click()

    time.sleep(3)
    
    # Obtener Partes
    rows_parte = driver.find_elements(By.XPATH, '//*[@id="expediente:participantsTable"]/tbody[contains(@class,"rf-dt-b")]')
    
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