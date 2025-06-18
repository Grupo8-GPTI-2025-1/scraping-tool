from driver import Driver
from selenium.webdriver.common.by import By
from time import sleep
from post_module import post_data, format_data


class PortalInmobiliarioScraper(Driver):
    def __init__(self):
        super().__init__()
        self.initialize_driver()
        self.link = 'https://www.portalinmobiliario.com'
        self.depto_links = 'https://www.portalinmobiliario.com/venta/departamento'
        self.depto_links_pag_2 = 'https://www.portalinmobiliario.com/venta/departamento/_Desde_49_NoIndex_True'

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
    
    def get_description(self) -> str:
        try:
            element = self.find_element(By.CLASS_NAME, 'ui-pdp-description__content')
            return element.get_attribute('textContent').strip()
        except Exception as e:
            print(f"[ERROR get_description]: {e}")
            return "Descripción no disponible"

    def get_data(self, link:str) -> dict:
        self.load_page(link)
        return {
            'name'      : self.get_title(),
            'type'      : 'departamento',
            'rooms'     : int(self.get_rooms('dormitorios')[0]) if self.get_rooms('dormitorios')[0].isdigit() else -1, 
            'bathrooms' : int(self.get_rooms('baños')[0]) if self.get_rooms('baños')[0].isdigit() else -1,
            'price'     : int(self.get_price().replace(".", "")),
            'location'  : self.get_location(),
            'description': self.get_description(),
            'url'       : link.split('#')[0]
        }
    
    def get_links_from_one_page(self, link: str) -> list:
        self.load_page(link)
        sleep(3)  # Espera a que la página cargue completamente
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

    def get_links(self) -> list:
        billboard_links = []
        billboard_links += self.get_links_from_one_page(self.depto_links)
        #billboard_links += self.get_links_from_one_page(self.depto_links_pag_2)
        return billboard_links
    
    def get_all_data(self) -> list:
        links = self.get_links()
        all_data = []
        for link in links:
            data = self.get_data(link)
            all_data.append(data)
        return all_data
    
    def post_portal(self, link: str) -> None:
        data = self.get_data(link)
        formatted_data = format_data(data, False)
        if formatted_data["rooms"] == 0 or formatted_data["price"] == 0:
            print(f"Error en la oferta: {link}")
            return
        post_data([formatted_data], 'http://localhost:4000/properties')

    def post_portals(self) -> None:
        links = self.get_links()
        print(f"Total de links a publicar: {len(links)}")
        for link in links:
            try:
                print(f"Publicando link: {link}")
                self.post_portal(link)
            except Exception as e:
                print(f"Error al publicar {link}: {e}")
