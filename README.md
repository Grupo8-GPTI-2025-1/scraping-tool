# Scrapping-tool

## Consideraciones
- Requiere que se instale selenium*: pip install selenium https://pypi.org/project/selenium/
- Se requiere de un archivo ".env" que contiene la url del backend en el valor API_URL (http://backend:4000)

(Nota: Si el modulo de selenium no es reconocido en VSCODE https://stackoverflow.com/questions/71324949/import-selenium-could-not-be-resolved-pylance-reportmissingimports)

# Ejecucion
- Ejecutar archivo main.py con el contenedor del backend (y por lo tanto la DB) corriendo. El scraper debería tomar 10 minutos más o menos, cargando aproximadamente 40 propiedades de Airbnb y 50 de Portal Inmobiliario

## pi_scraper.py
Scraper encargado de recopilar la información de la página del Portal Inmobiliario

## airbnb.py
Scraper encargado de recopilar la información de la página del Airbnb.

## driver.py
Clase padre de ambos scrapers, con los métodos necesarios para su correcto funcionamiento.

## post_module-py
Módulo contenedor de funciones asociadas a la carga de datos a través del backend a la DB, a través de métodos post.

## scraper.py (no se utiliza)
Archivo de legado. Si llegara a no funcionar main.py, probar directamente con este.

# archivist.py (no se utiliza)
Codigo de scrapping, se encarga de leer las urls del input_file, usar las clases Driver del modulo scraper y postear los datos formateados a la base de datos

Requiere que se instale selenium: https://pypi.org/project/selenium/

Si el modulo no es reconocido: https://stackoverflow.com/questions/71324949/import-selenium-could-not-be-resolved-pylance-reportmissingimports
