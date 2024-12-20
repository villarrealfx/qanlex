[Aquí la versión en Español del README](README.md)
# Qanlex - Qanlex - Web Scraping System Development

**Task: Develop a web scraper for a page provided by the company to extract relevant information about lawsuits on the site.**

## Index

* **Introduction**
* **Features**
* **Limitations**
* **Installation**
* **Bibliography**


## Introduction

* **What is the project?**
    * The project consists of coding a script for the automated extraction of information related to Lawsuits from a webpage provided by the company.
* **Why did you create it**
    * At the request of Qanlex company as an exercise for applicants.
* **Main objective**
    * __Scraper Development:__ Create a functional scraper that extracts at least: Case number, Department, Plaintiff, Defendant, Title, Type of lawsuit, Court, and relevant dates. The scraper should search for "Party", in the "COM" Jurisdiction, using the keyword "RESIDUOS". The results should be saved in a table.

    * __Code Quality:__ I value clean, well-structured code that follows good programming practices.

    * __Documentation:__ nclude comments and/or documentation that facilitate the understanding and maintenance of the code, as well as anything you have assumed from the exercise.

## Features

* **Customizable:** Allows you to configure the search by j**`jurisdicción`** y **`parte`**.
* **Robust:** Handles common errors such as changes in the website structure.
* **Scalable:** Can be adapted to extract data from multiple pages.
* **Flexible:** The extracted data can be exported in different formats (CSV, JSON, etc.).

* **Main features**
    1. Automate data extraction: From a specific webpage, using `Selenium` to interact with dynamic elements.
    2. Organize data: The extracted data is stored in a data structure (table) and then exported to a **`CSV`** file.
    3. Customize the search: Allows the user to specify search criteria such as **`jurisdicción`** y **`parte`**.
* **Project Structure**
    * **`src`**: Contains the main script and utility functions.
    * **`data`**: Stores the extracted data.
* **Key Functions**
    * `start_chrome()`: Initializes the Chrome browser with the configured options.
    * `recapcha(driver)`: Handles reCAPTCHA resolution (specific implementation).
    * `get_information(driver)`: Extracts data from an individual case.
    * `get_table_actuaciones()`: Extracts actions related to a case.
    * `get_intervinientes()`: Extracts the intervening parties in a case.
    * `list_to_table()`: Converts the list of cases into a CSV format and saves it to a file.
* **Data Extraction Flow**

    1. **`Start`**: The script starts and an instance of WebDriver is created to control the Chrome browser.
    2. **`Access to the page`**: Accesses the target webpage and locates the search form.
    3. **`Data entry`**: The form is filled with the specified search criteria.
    4. **`Resolving reCAPTCHA`**: The reCAPTCHA is activated and the user is expected to resolve it manually.
    5. **`Search`**: The search form is submitted and the list of results is obtained.
    6. **`Data extraction`**: For each case in the results list:
        * Accesses the detailed page of the case.
        * Extracts relevant data using XPath or CSS selectors.
        * Stores the information in a data structure.
        * Report generation: The collected data is exported to a CSV file.
* **Structure of the extracted data**
    1. **`expediente_numero`**: Case number.
    2. **`jurisdicción`**: Jurisdiction of the case.
    3. **`dependencia`**: Department in charge of the case.
    4. **`situacion_actual`**: Current status of the case.
    5. **`caratula`**: Case title.
    6. **`actuaciones`**: List of actions related to the case (obtained from the get_table_actuaciones function).
    7. **`intervinientes`**: List of intervening parties in the case (obtained from the get_intervinientes function).

## Limitations

* The main limitation of the script is the resolution of the reCAPTCHA, which must be done manually. To overcome this limitation, the feasibility of **`using third-party CAPTCHA resolution services`** can be studied. These services automate the resolution of these security challenges, allowing scripts to continue running without interruption.

* Popular services include::
    * 2Captcha
    * Anti-Captcha
    * DeathByCaptcha
    * CapMonster

## Installation

1. **Clone the repository:**

``` bash
    git clone https://github.com/villarrealfx/qanlex.git
```
2. **Create a virtual environment:**

``` bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
```
3. **Install dependencies:**

``` bash
    pip install -r requirements.txt
```
4. **Configure the config.py file:**
The script is set to work correctly according to the requested parameters, however, there is the possibility of making adjustments in the configuration file `config.py`

    * `URL`: Enter the base URL of the website.
    * `ID y XPath`: Update the identifiers and XPath expressions according to the website structure.
    * `Other parameters`: Configure any other parameters required for the search (jurisdiction, party, etc.).

5. **Run Script**
```bash
    python src/scrape.py
```

## Bibliography

### Websites
1. https://stackoverflow.com/
2. https://www.selenium.dev/documentation/
3. https://docs.python.org/3/

### Books
1. Learning Selenium Testing Tools with Python | Unmesh Gundecha | Packt Publishing.
2. Pandas-Cookbook-eBook (2017) | Theodore Petrou | Packt Publishing
3. Data Engineering with Python (2020) | Paul Crickard | Packt Publishing

<hr>

