from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Driver:
    def __init__(self):
        self.options = Options()
        self.driver = None

    def initialize_driver(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.delete_all_cookies()
        self.driver.maximize_window()

    def load_page(self, page: str) -> None:
        self.driver.get(page)
        #sleep(2)

    def click_element(self, by: str, xpath: str) -> None:
        sleep(1)
        element = self.driver.find_element(by=by, value=xpath)
        element.click()

    def write_element(self, by: str, xpath: str, content: str):
        sleep(1)
        self.driver.find_element(by=by, value=xpath).send_keys(content)

    def find_element(self, by: str, xpath: str) -> WebElement:
        return self.driver.find_element(by=by, value=xpath)
    
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        sleep(5)

    def close(self) -> None:
        self.driver.quit()
        self.driver = None


class PortalInmobiliarioScraper(Driver):
    def __init__(self):
        super().__init__()
        self.initialize_driver()
        self.link = 'https://www.portalinmobiliario.com'
        self.depto_links = 'https://www.portalinmobiliario.com/venta/departamento'

    def get_title(self) -> str:
        value = "//div[@class='ui-pdp-header__title-container']"
        elemento = self.find_element(By.XPATH, value)
        return elemento.get_attribute('textContent').strip('Agregar a favoritos')
    
    def get_rooms(self, tipo='dormitorios') -> str:
        value = f"//div[@class='ui-pdp-highlighted-specs-res']"
        value_t = f"//span[contains(text(), '{tipo}')]"
        element = self.find_element(By.XPATH, value)
        return element.find_element(By.XPATH, value_t).get_attribute('textContent')
    
    def get_price(self) -> str:
        return self.driver.find_element(By.ID, 'price').get_attribute('textContent').split('$')[1]

    
    def get_location(self) -> str:
        element = self.find_element(By.CLASS_NAME, 'ui-vip-location__subtitle')
        return element.get_attribute('textContent').strip('Ver información de la zona')

    def get_data(self, link:str) -> dict:
        self.load_page(link)
        return {
            'name'      : self.get_title(),
            'type'      : 'departamento',
            'rooms'     : self.get_rooms('dormitorios'), 
            'bathrooms' : self.get_rooms('baños'),
            'price'     : self.get_price(),
            'location'  : self.get_location(),
            'url'       : link.split('#')[0]
        }
    
    def get_links(self) -> list:
        self.load_page(self.depto_links)
        data = self.find_element(By.CLASS_NAME, 'ui-search-results')
        datos = data.find_elements(By.CLASS_NAME, 'ui-search-layout__item')
        print(f"Total de elementos encontrados: {len(datos)}")
        billboard_links = []
        for dato in datos:
            try:
                link_elem = dato.find_element(By.XPATH, ".//a[contains(@class, 'poly-component__badge poly-component__badge--image poly-component__link')]")
                href = link_elem.get_attribute("href")
                billboard_links.append(href)
            except Exception as e:
                print(f"Error: {e}")
                continue
        return billboard_links
    
    def get_all_data(self) -> list:
        links = self.get_links()
        all_data = []
        for link in links:
            data = self.get_data(link)
            all_data.append(data)
        return all_data

class AirbnbScraper(Driver):
    def __init__(self):
        super().__init__()
        self.initialize_driver()
        self.link = 'https://www.airbnb.cl'
        self.depto_links = 'https://www.airbnb.cl//s/Santiago-de-Chile--Santiago/homes?refinement_paths%5B%5D=%2Fhomes&acp_id=t-g-ChIJBaYeX77FYpYREEZwTeVOE_A&date_picker_type=calendar&source=structured_search_input_header&search_type=user_map_move&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-06-01&monthly_length=3&monthly_end_date=2025-09-01&price_filter_input_type=2&channel=EXPLORE&place_id=ChIJBaYeX77FYpYREEZwTeVOE_A&query=Santiago%20de%20Chile%2C%20Santiago&search_mode=regular_search&price_filter_num_nights=5&ne_lat=-33.310872118077114&ne_lng=-70.53990055531199&sw_lat=-33.58297011852006&sw_lng=-70.79099137470294&zoom=10.99720104082905&zoom_level=10.99720104082905&search_by_map=true'

    def get_title(self) -> str:
        value = self.driver.find_element(By.XPATH, "//h1").text.strip()
        return value
                
    def get_price(self) -> str:
        try:
            wait = WebDriverWait(self.driver, 30)
            # Espera un span que contenga 'CLP' dentro de un botón
            spans = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//button//span[contains(text(), 'CLP')]"
            )))
            
            for i, span in enumerate(spans):
                if span.text and "CLP" in span.text:
                    if span.text.strip() == "CLP":
                        return "Precio no encontrado"
                    return span.text.strip().strip("CLP").strip("$").replace(',', '.')              

            return "Precio no encontrado"
        except Exception as e:
            print(f"[ERROR get_price]: {e}")
            return "Error al obtener precio"
        
    def find_rooms_and_bathrooms(self, item: WebElement) -> tuple:
        habitaciones = '1 habitación'
        baños = 'compartido'
        for i in item:
            if 'habitaci' in i.text.lower():
                habitaciones = i.text.strip("· ")
            elif 'baño' in i.text.lower():
                baños = i.text.strip("· ")
        return habitaciones, baños


    def get_data(self, link:str) -> dict:
        self.load_page(link)

        wait = WebDriverWait(self.driver, 10)
        resumen = wait.until(EC.presence_of_element_located((
            By.XPATH, "//li[contains(@class, 'l7n4lsf')]"
        )))

        resumen = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'l7n4lsf')]")
        habitaciones, baños = self.find_rooms_and_bathrooms(resumen)

        return {
            'name'      : self.get_title(),
            'type'      : 'departamento',
            'rooms'     : habitaciones, 
            'bathrooms' : baños,
            'price'     : self.get_price(),
            'url'       : link.split('#')[0]
        }
    
    def get_links(self) -> list:
        self.load_page(self.depto_links)
        wait = WebDriverWait(self.driver, 30)

        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        links_set = set()

        while True:
            # Scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)

            # Obtener todos los elementos tipo /rooms/
            elems = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/rooms/')]")
            for elem in elems:
                href = elem.get_attribute("href")
                if href and "/rooms/" in href:
                    links_set.add(href)  # limpia parámetros

            # Verificar si ya no hay más scroll
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        billboard_links = list(links_set)
        print(f"Total de links encontrados: {len(billboard_links)}")
        return billboard_links
    
    def get_all_data(self) -> list:
        links = self.get_links()
        all_data = []
        for link in links:
            data = self.get_data(link)
            all_data.append(data)
        return all_data


if __name__ == '__main__':
    print('Scrap de una oferta ')
    scraper = PortalInmobiliarioScraper()
    all_data_portal = scraper.get_all_data()
    print(all_data_portal)

    scraper.close()