import time

# Automatiza instalación de chorme driver
from webdriver_manager.chrome import ChromeDriverManager

#Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#Modificar opciones de webdriver Chrome
from selenium.webdriver.chrome.options import Options
# Definir tipo de busqueda
from selenium.webdriver.common.by import By

# https://www.google.com/search?q=youtube%3A+proyecto+completo+de+web+scraping+con+selenium&oq=youtube%3A+proyecto+completo+de+web+scraping+con+selenium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg60gEJMTc2NjNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

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
    options.add_argument('--headless')
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


# MAIN
if __name__ == '__main__':
    driver = start_chrome()
    url = 'https://articulo.mercadolibre.com.ve/MLV-767782546-oferta-combo-tarjeta-madre-h81-core-i7-fan-cooler-8gb-_JM#polycard_client=search-nordic&position=2&search_layout=grid&type=item&tracking_id=8d625a57-b631-43a3-8e25-1faf719bee02'
    driver.get(url)
    input('ingrese el catcha y pulse enter.....')
    # Inicio Scraper
    nombre_producto = driver.find_element(By.CSS_SELECTOR, 'h1.ui-pdp-title').text
    precio_producto = driver.find_element(By.CSS_SELECTOR, 'span.ui-pdp-price__part').text

    # print(f'Nombre Producto: {nombre_producto}')
    # print(f'Precio Producto: {precio_producto}')
    
    driver.quit()

    lista = precio_producto.split()
    print(lista)












