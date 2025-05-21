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
        return self.driver.find_element(By.ID, 'price').get_attribute('textContent')
    
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
        print(billboard_links)
        return billboard_links

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
            wait = WebDriverWait(self.driver, 20)
            # Espera un span que contenga 'CLP' dentro de un botón
            spans = wait.until(EC.presence_of_all_elements_located((
                By.XPATH, "//button//span[contains(text(), 'CLP')]"
            )))
            
            for i, span in enumerate(spans):
                if span.text and "CLP" in span.text:
                    return span.text.strip()

            return "Precio no encontrado"
        except Exception as e:
            print(f"[ERROR get_price]: {e}")
            return "Error al obtener precio"

    def get_data(self, link:str) -> dict:
        self.load_page(link)

        wait = WebDriverWait(self.driver, 10)
        resumen = wait.until(EC.presence_of_element_located((
            By.XPATH, "//li[contains(@class, 'l7n4lsf')]"
        )))

        resumen = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'l7n4lsf')]")

        for item in resumen:
            if "habitaci" in item.text.lower():
                habitaciones = item.text.split(' ')[2]

            if "baño" in item.text.lower():
                baños = item.text.split(' ')[2]

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
        datos = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/rooms/')]")
        print(f"Total de elementos encontrados: {len(datos)}")
        billboard_links = []
        for dato in datos:
            try:
                href = dato.get_attribute("href")
                billboard_links.append(href)
            except Exception as e:
                print(f"Error: {e}")
                continue
        print(billboard_links)
        return billboard_links


if __name__ == '__main__':
    print('Scrap de una oferta ')
    scraper = AirbnbScraper()
    data = scraper.get_data("https://www.airbnb.cl/rooms/1296471826558499503?search_mode=regular_search&adults=1&check_in=2025-05-26&check_out=2025-05-31&children=0&infants=0&pets=0&source_impression_id=p3_1747844899_P3tnZeHe4c7p52G7&previous_page_section_name=1000&federated_search_id=db2785f1-768e-404c-a79a-f8b06853e22f")
    print(data)
    data = scraper.get_data("https://www.airbnb.cl/rooms/1330590650199610252?search_mode=regular_search&adults=1&check_in=2025-05-21&check_out=2025-05-26&children=0&infants=0&pets=0&source_impression_id=p3_1747843939_P3JmVfVudOA9huWX&previous_page_section_name=1000&federated_search_id=3737772c-479b-4fcf-a032-39fa30acbdc0")
    print(data)
    scraper.close()