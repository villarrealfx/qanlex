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
    
    captcha = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
    value = captcha.get_attribute("aria-checked")
    print(f'valor de atributo "aria-checked" Inicial: {value}')

    while value == 'false':
        time.sleep(0.5)
        captcha = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
        value = captcha.get_attribute("aria-checked")
        print(f'valor de atributo "aria-checked" Inicial: {value}')

    return True