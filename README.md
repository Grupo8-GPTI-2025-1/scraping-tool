# Scrapping-tool

## Consideraciones
- Requiere que la librería selenium esté instalada: `pip install selenium` (https://pypi.org/project/selenium/)
- Se requiere que esté instalada la libreria python-dotenv: `pip install dotenv` (https://pypi.org/project/python-dotenv/)
- Se requiere un archivo ".env" con la url del backend (http://backend:4000 para Docker) en la variable `API_URL`

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
