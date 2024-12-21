[Here README English version](README_EN.md)             

# Qanlex - Desarrollo de sistema de scraper web

**La tarea es desarrollar un scraper web para una página suministrada por la empresa con el objetivo es extraer información relevante sobre demandas presentes en el sitio.**

## Índice

* **Introducción**
* **Características**
* **Limitaciones**
* **Instalación**
* **Bibliografía**


## Introducción

* **¿Qué es el proyecto?**
    * El proyecto consiste en la codificación de un script para la extración automatizada de información referente a Demandas desde una pagina web suministrada por la empresa.
* **Por qué lo creaste**
    * A solicitud de la empresa Qanlex como ejercicio para aplicantes
* **Objetivo principal**
    * __Desarrollo del Scraper:__ Crear un scraper funcional que extraiga al menos: Expediente, Dependencia, Demandante, demandado, caratula, tipo de demanda, juzgado o tribunal y fechas relevantes. El scraper debe buscar “Parte”, en la Jurisdiccion “COM”, utilizando la palabra clave “RESIDUOS”. Los resultados deben ser guardados en una tabla.

    * __Calidad del Código:__ Valoramos un código limpio, bien estructurado y siguiendo buenas prácticas de programación.

    * __Documentación:__ Incluye comentarios y/o documentación que faciliten la comprensión y mantenimiento del código, así como cualquier cosa que hayas asumido del ejercicio.

## Características

* **Personalizable:** Permite configurar la búsqueda por jurisdicción y parte.
* **Robusto:** Maneja errores comunes como cambios en la estructura de la página web.
* **Escalable:** Puede adaptarse para extraer datos de múltiples páginas.
* **Flexible:** Los datos extraídos se pueden exportar en diferentes formatos (CSV, JSON, etc.).

* **Características principales**
    1. Automatizar la extracción de datos: De una página web específica, utilizando **`Selenium`** para interactuar con elementos dinámicos.
    2. Organizar los datos: Los datos extraídos son almacenados en una estructura de datos (tabla) y luego exportados a un archivo **`CSV`**.
    3. Personalizar la búsqueda: Permite al usuario especificar criterios de búsqueda como **`jurisdicción`** y **`parte`**.
* **Estructura del Proyecto**
    * **`src`**: Contiene el script principal y las funciones de utilidad.
    * **`data`**: Almacena los datos extraídos.
* **Funciones Clave**
    * `start_chrome()`: Inicializa el navegador Chrome con las opciones configuradas.
    * `recapcha(driver)`: Maneja la resolución del reCAPTCHA (implementación específica).
    * `get_information(driver)`: Extrae los datos de un expediente individual.
    * `get_table_actuaciones()`: Extrae las actuaciones relacionadas con un expediente.
    * `get_intervinientes()`: Extrae los intervinientes en un expediente.
    * `list_to_table()`: Convierte la lista de expedientes en un formato CSV y lo guarda en un archivo.
* **Flujo de Ejecución**
    1. **`Inicio`**: Se inicia el script y se crea una instancia de WebDriver para controlar el navegador Chrome.
    2. **`Acceso a la página`**: Se accede a la página web objetivo y se localiza el formulario de búsqueda.
    3. **`Ingreso de datos`**: Se completa el formulario con los criterios de búsqueda especificados.
    4. **`Resolución de reCAPTCHA`**: Se activa el reCAPTCHA y se espera a que el usuario lo resuelva manualmente.
    5. **`Búsqueda`**: Se envía el formulario de búsqueda y se obtiene la lista de resultados.
    6. **`Extracción de datos`**: Para cada expediente en la lista de resultados:
        * Se accede a la página detallada del expediente.
        * Se extraen los datos relevantes utilizando XPath o CSS selectors.
        * Se almacena la información en una estructura de datos.
        * Generación del reporte: Los datos recopilados se exportan a un archivo CSV.
* **Estructura de los datos extraidos**
    1. **`expediente_numero`**: Número del expediente.
    2. **`jurisdicción`**: Jurisdicción del expediente.
    3. **`dependencia`**: Dependencia encargada del expediente.
    4. **`situacion_actual`**: Situación actual del expediente.
    5. **`caratula`**: Carátula del expediente.
    6. **`actuaciones`**: Lista de actuaciones relacionadas con el expediente (obtenida de la función get_table_actuaciones).
    7. **`intervinientes`**: Lista de intervinientes en el expediente (obtenida de la función get_intervinientes).

## Limitaciones

* La principal limitación del script es la resolución del `reCAPTCHA`el cual se debe realizar de forma manual, para saltar esta limitación se puede estudiar la viabilidad de usar los **servicios de resolución de CAPTCHA por terceros** que son herramientas que automatizan la resolución de estos desafíos de seguridad, permitiendo a los scripts continuar con su ejecución sin interrupciones. Estos servicios suelen utilizar técnicas de reconocimiento de patrones, aprendizaje automático o incluso la intervención humana para resolver los CAPTCHA.

* Servicios Populares:
    * 2Captcha: Uno de los servicios más conocidos, ofrece una amplia gama de soluciones para diferentes tipos de CAPTCHA, incluyendo reCAPTCHA.
    * Anti-Captcha: Otro servicio popular, con una API fácil de usar y soporte para múltiples lenguajes de programación.
    * DeathByCaptcha: Similar a 2Captcha, ofrece resolución de CAPTCHA a través de una API.
    * CapMonster: Ofrece una variedad de soluciones para la resolución de CAPTCHA, incluyendo servicios en la nube y software local.

* Se ha realizado una aproximación al despliegue en los servicios de AWS por favor lea el [README AWS haciendo click aquí](aws/README.md) el cual se ve afectado por la limitación de la resolución del reCAPTCHA.

## Instalación

1. **Clonar el repositorio:**

``` bash
    git clone https://github.com/villarrealfx/qanlex.git
```
2. **Crear un entorno virtual:**

``` bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
```
3. **Instalar las dependencias:**

``` bash
    pip install -r requirements.txt
```
4. **Configurar el archivo config.py:**
El script se encuentra seteado para funcionar correctamente según los parámetros solicitados sin embargo existe la posibilidad de realizar ajustes en el archivo de configuración `config.py`

    * `URL`: Ingresar la URL base del sitio web.
    * `ID y XPath`: Actualizar los identificadores y expresiones XPath según la estructura del sitio web.
    * `Otros parámetros`: Configurar cualquier otro parámetro necesario para la búsqueda (jurisdicción, parte, etc.).

5. **Ejecutar Script**
```bash
    python src/scrape.py
```
python src/scrape.py
## Bibliografía

### Websites
1. https://stackoverflow.com/
2. https://www.selenium.dev/documentation/
3. https://docs.python.org/3/

### Libros
1. Learning Selenium Testing Tools with Python | Unmesh Gundecha | Packt Publishing.
2. Pandas-Cookbook-eBook (2017) | Theodore Petrou | Packt Publishing
3. Data Engineering with Python (2020) | Paul Crickard | Packt Publishing

<hr>

