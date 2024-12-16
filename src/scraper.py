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

from funtions.utils import start_chrome, recapcha
from funtions.config import URL, ID_FORM_PUBLICA, ID_JURIDICCION, select_jurid, tex_parte, ID_PARTE, ID_BUSCAR

# https://www.google.com/search?q=youtube%3A+proyecto+completo+de+web+scraping+con+selenium&oq=youtube%3A+proyecto+completo+de+web+scraping+con+selenium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg60gEJMTc2NjNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8




# MAIN
if __name__ == '__main__':
    print('INICIO DE SCRAPING'.center(80, '#'))
    print('#'*80)
    driver = start_chrome()
    wait = WebDriverWait(driver, 50)
    driver.get(URL)
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

    # random.random()
    time.sleep(random.uniform(0.75,3))
    
    print('Solucionando reCAPCHA ......')
    # Seleccionar reCAPCHA
    driver.switch_to.frame(0)
    driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]').click()

    value = recapcha(driver)
    # while value == False:
    #     value = recapcha(driver)

    print('reCAPCHA Resuelto ......')
    print(value, type(value))


    driver.switch_to.default_content()
    button.click()
    print('Entrando a pagina de consulta ......')

    input('espera y pulsa enter.....')

    driver.quit()












