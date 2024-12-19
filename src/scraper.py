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

from funtions.utils import start_chrome, recapcha, get_information
from funtions.config import URL, ID_FORM_PUBLICA, ID_JURIDICCION, select_jurid, tex_parte, ID_PARTE, ID_BUSCAR


# MAIN
if __name__ == '__main__':
    
    inicio = time.time()

    print('  INICIO DE SCRAPING  '.center(80, '#'))
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
    time.sleep(random.uniform(1.3,4))
    
    print('Solucionando reCAPCHA ......')
    # Seleccionar reCAPCHA
    driver.switch_to.frame(0)
    driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]').click()

    value = recapcha(driver)
    # while value == False:
    #     value = recapcha(driver)

    print('reCAPCHA Resuelto ......')
    
    driver.switch_to.default_content()
    button.click()
    print('Entrando a pagina de consulta ......')

    # Trabajar con Tabla
    # Identificar Filas de tabla
    rows = driver.find_elements(By.XPATH, '//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr')
    columns = driver.find_elements(By.XPATH, '//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr[1]/td')

    print(f"Filas {len(rows)} y columnas {len(columns)}")

    expedientes = []

    btt_pag = 'Siguiente'

    while btt_pag == 'Siguiente':

        for i in range(1, 3): #len(rows)+1):

            # time.sleep(10)
            wait.until(ec.element_to_be_clickable((By.XPATH, f'//*[@id="j_idt118:j_idt119:dataTable"]/tbody/tr[{i}]/td[6]/div/a')))
            time.sleep(5)
            
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
            


    print(expedientes)

    final =time.time()
    print(f'Tiempo de duración de procesamiento: {final - inicio} segundos')
    input('espera y pulsa enter.....')

    driver.quit()












