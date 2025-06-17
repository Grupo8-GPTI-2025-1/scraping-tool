# Scrapping-tool

## Consideraciones
- Requiere que se instale selenium*: pip install selenium https://pypi.org/project/selenium/
- Se requiere de un archivo ".env" que contiene la url del backend en el valor API_URL

(Nota: Si el modulo de selenium no es reconocido en VSCODE https://stackoverflow.com/questions/71324949/import-selenium-could-not-be-resolved-pylance-reportmissingimports)

# Ejecucion
- Crear un archivo "input_file.txt" con las direcciones que se quiere scrapear, ya sea airbnb o portal inmobiliario (el codigo distingue por si solo)
- Crear un archivo ".env" con la dirección de la base de datos a la que se quiere hacer los request
- Ejecutar `python archivist.py` en la consola

# archivist.py
Codigo de scrapping, se encarga de leer las urls del input_file, usar las clases Driver del modulo scraper y postear los datos formateados a la base de datos

## scraper.py
Herramienta de scrapping, puede obtener los datos de una propiedad

Requiere que se instale selenium: https://pypi.org/project/selenium/

Si el modulo no es reconocido: https://stackoverflow.com/questions/71324949/import-selenium-could-not-be-resolved-pylance-reportmissingimports