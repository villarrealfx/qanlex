import time
import random

# Definir tipo de busqueda
from selenium.webdriver.common.by import By
# Manejar opciones de Select
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from funtions.utils import start_chrome, recapcha, get_information, clear, list_to_table
from funtions.config import URL, ID_FORM_PUBLICA, ID_JURIDICCION,  ID_PARTE, ID_BUSCAR, XP_RECAPCHA, XP_DATATABLE, XP_DATATABLE_COLUM, select_jurid, tex_parte, jurisdi


# MAIN
if __name__ == '__main__':
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

        # random.random()
        time.sleep(random.uniform(1.3,4))
        
        rellenar_información = time.time()

        print('Solucionando reCAPCHA ......')
        # Seleccionar reCAPCHA
        driver.switch_to.frame(0)
        driver.find_element(By.XPATH, XP_RECAPCHA).click()

        value = recapcha(driver)
        # if value == False:

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

        # print(f"Filas {len(rows)} y columnas {len(columns)}")

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
                
        file = list_to_table(expedientes)

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




    except Exception as e: 
        # Manejar otros errores de análisis 
        print ( f'Error ocurrido al analizar HTML: {e} ' ) 
        
    finally : 
        # Cerrar la instancia de webdriver
        driver.quit()


    












