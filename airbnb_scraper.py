from driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from post_module import post_data, format_data


class AirbnbScraper(Driver):      

    def __init__(self):
        super().__init__()
        self.initialize_driver()
        self.link = 'https://www.airbnb.cl'
        self.depto_links = 'https://www.airbnb.cl//s/Santiago-de-Chile--Santiago/homes?refinement_paths%5B%5D=%2Fhomes&acp_id=t-g-ChIJBaYeX77FYpYREEZwTeVOE_A&date_picker_type=calendar&source=structured_search_input_header&search_type=user_map_move&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-06-01&monthly_length=3&monthly_end_date=2025-09-01&price_filter_input_type=2&channel=EXPLORE&place_id=ChIJBaYeX77FYpYREEZwTeVOE_A&query=Santiago%20de%20Chile%2C%20Santiago&search_mode=regular_search&price_filter_num_nights=5&ne_lat=-33.310872118077114&ne_lng=-70.53990055531199&sw_lat=-33.58297011852006&sw_lng=-70.79099137470294&zoom=10.99720104082905&zoom_level=10.99720104082905&search_by_map=true'
        self.depto_links_pag_2 = 'https://www.airbnb.cl/s/Santiago-de-Chile--Santiago/homes?refinement_paths%5B%5D=%2Fhomes&acp_id=t-g-ChIJBaYeX77FYpYREEZwTeVOE_A&date_picker_type=calendar&source=structured_search_input_header&search_type=user_map_move&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-07-01&monthly_length=3&monthly_end_date=2025-10-01&price_filter_input_type=2&channel=EXPLORE&place_id=ChIJBaYeX77FYpYREEZwTeVOE_A&query=Santiago%20de%20Chile%2C%20Santiago&search_mode=regular_search&price_filter_num_nights=5&ne_lat=-33.310872118077114&ne_lng=-70.53990055531199&sw_lat=-33.58297011852006&sw_lng=-70.79099137470294&zoom=10.99720104082905&zoom_level=10&search_by_map=true&federated_search_session_id=891d0d5f-c8fa-4835-b34f-ba3dd64ac852&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxOCwidmVyc2lvbiI6MX0%3D'

    def get_title(self) -> str:
        value = self.driver.find_element(By.XPATH, "//h1").text.strip()
        return value
    
    def get_description(self) -> str:
        try:
            value = self.driver.find_element(By.XPATH, "//span[@class='l1h825yc atm_kd_19r6f69_24z95b atm_kd_19r6f69_1xbvphn_1oszvuo dir dir-ltr']").text.strip()
            return value if value else "Descripción no disponible"
        except Exception as e:
            print(f"[ERROR get_description]: {e}")
            return "Descripción no disponible"
                
    def get_price(self) -> str:
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
        
    def find_rooms_and_bathrooms(self, item: WebElement) -> tuple:
        habitaciones = "1"
        baños = "0"
        huespedes = "1"
        for i in item:
            if 'habitaci' in i.text.lower():
                habitaciones = i.text.strip("· ")
            elif 'baño' in i.text.lower():
                baños = i.text.strip("· ")
            elif 'huésped' in i.text.lower():
                huespedes = i.text.strip("· ")
        return habitaciones, baños, huespedes


    def get_data(self, link:str) -> dict:
        self.load_page(link)
        sleep(3)  # Espera a que la página cargue completamente

        wait = WebDriverWait(self.driver, 10)
        resumen = wait.until(EC.presence_of_element_located((
            By.XPATH, "//li[contains(@class, 'l7n4lsf')]"
        )))

        resumen = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'l7n4lsf')]")
        habitaciones, baños, huespedes = self.find_rooms_and_bathrooms(resumen)

        return {
            'name'      : self.get_title(),
            'type'      : 'departamento',
            'rooms'     : int(habitaciones[0]) if habitaciones[0].isdigit() else 0,
            'bathrooms' : int(baños[0]) if baños[0].isdigit() else 0,
            'price'     : float(self.get_price().replace(".", "")) if self.get_price() != "Precio no encontrado" else 0,
            'url'       : link.split('#')[0],
            'description': self.get_description(),
            'guests'    : int(huespedes[0]) if huespedes[0].isdigit() else 0
        }
    
    def get_links_of_one_page(self, link: str) -> list:
        self.load_page(link)
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
    
    def get_links(self) -> list:
        billboard_links = []
        billboard_links += self.get_links_of_one_page(self.depto_links)
        billboard_links += self.get_links_of_one_page(self.depto_links_pag_2)
        return billboard_links
    
    def get_all_data(self) -> list:
        links = self.get_links()
        all_data = []
        for link in links:
            data = self.get_data(link)
            all_data.append(data)
        return all_data
    
    def post_airbnb(self, link: str) -> None:
        data = self.get_data(link)
        formatted_data = format_data(data, True)
        if formatted_data["rooms"] == 0 or formatted_data["price"] == 0:
            print(formatted_data)
            print(f"Error en la oferta: {link}")
            return
        post_data([formatted_data], 'http://localhost:4000/airbnbs')

    def post_airbnbs(self) -> None:
        links = self.get_links()
        print(f"Total de links a publicar: {len(links)}")
        for link in links:
            try:
                print(f"Publicando link: {link}")
                self.post_airbnb(link)
            except Exception as e:
                print(f"Error al publicar {link}: {e}")