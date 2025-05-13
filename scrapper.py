from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
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
        
    def find_elements(self, by: str, xpath: str):
        return self.driver.find_elements(by=by, value=xpath)
    
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
        self.link = 'https://www.airbnb.cl/'
        self.depto_links = None

    def get_title(self) -> str:
        value = "//div[@data-section-id='TITLE_DEFAULT']" 
        titulo = self.find_element(By.XPATH, value)
        #titulo = elemento.find_element(By.XPATH, "//h2[@tabindex='1']")
        return titulo.get_attribute('textContent').strip('CompartirGuardar')
    
    def details(self) -> str:
        value = '/*[@data-section-id="OVERVIEW_DEFAULT_V2"]'
        overview = self.find_element(By.XPATH, value)#.find_element(By.TAG_NAME, 'ol')
        elements = overview.get_attribute('textContent')#find_elements(By.TAG_NAME, "li")
        print(elements)
        # value_g = f"//*[contains(text(), 'sped')]" 
        # value_h = f"//*[contains(text(), 'habitaci')]"
        # value_c = f"//*[contains(text(), 'cama')]"
        # value_b = f"//*[contains(text(), 'baño')]"/html/body/div[5]/div/div/div[1]/div/div/div[1]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]
        # details = {
        #     'guests'    : overview.find_element(By.XPATH, value_g),
        #     'rooms'     : overview.find_element(By.XPATH, value_h).get_attribute('textContent'),
        #     'bathrooms' : overview.find_element(By.XPATH, value_c).get_attribute('textContent'),
        #     'beds'      : overview.find_element(By.XPATH, value_b)
        # }
        # return details
        return elements

    
    def get_data(self, link:str) -> dict:
        self.load_page(link)
        #detalles = self.details()  # con errores
        return {
            'name'      : self.get_title(),
            'type'      : 'departamento',
            # 'rooms'     : detalles['rooms'], 
            # 'bathrooms' : detalles['bathrooms']
            # 'price'     : self.get_price(),
            # 'location'  : self.get_location(),
            # 'url'       : link.split('#')[0]
        }


if __name__ == '__main__':
    print('Scrap de una oferta ')
    offer = 'https://www.airbnb.cl/rooms/1373272437807452894' #input('Link: ') # 
    # scraper_p = PortalInmobiliarioScraper()
    scraper_a = AirbnbScraper()
    data = scraper_a.get_data(offer)
    # data = scraper_p.get_data(offer)
    print(data)
    #scraper.get_links()
    scraper_a.close()