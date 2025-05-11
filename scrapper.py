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
        sleep(5)

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

class PortalInmobiliarioScraper:
    def __init__(self):
        self.link = 'https://www.portalinmobiliario.com/venta/departamento'
        self.driver = Driver()
        self.driver.initialize_driver()

    def load_page(self, id: str) -> None:
        self.driver.load_page(self.link + id)

    def get_links(self) -> list:
        self.load_page(self.link)
        data = self.driver.find_element(By.CLASS_NAME, 'ui-search-results')
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


    def close(self) -> None:
        self.driver.close()


print("hello world")

if __name__ == '__main__':
    scraper = PortalInmobiliarioScraper()
    scraper.get_links()
    scraper.close()
    sleep(5)


#https://www.airbnb.cl/?refinement_paths%5B%5D=%2Fhomes&
#search_mode=flex_destinations_search&flexible_trip_lengths%5B%5D=one_week&location_search=MIN_MAP_BOUNDS&monthly_start_date=2025-06-01&monthly_length=3&monthly_end_date=2025-09-01&category_tag=Tag%3A789&price_filter_input_type=2&channel=EXPLORE&room_types%5B%5D=Entire%20home%2Fapt&selected_filter_order%5B%5D=room_types%3AEntire%20home%2Fapt&selected_filter_order%5B%5D=min_bedrooms%3A3&selected_filter_order%5B%5D=min_beds%3A1&selected_filter_order%5B%5D=min_bathrooms%3A3&update_selected_filters=false&search_type=filter_change&min_bedrooms=3&min_beds=0&min_bathrooms=3

#https://www.airbnb.cl/s/Barrio-El-Golf--Las-Condes/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-06-01&monthly_length=3&monthly_end_date=2025-09-01&price_filter_input_type=2&channel=EXPLORE&update_selected_filters=false&search_type=filter_change&price_filter_num_nights=5&place_id=ChIJcR_7EjzPYpYRwJzYztmtag8&acp_id=t-g-ChIJcR_7EjzPYpYRwJzYztmtag8&date_picker_type=calendar&query=Barrio%20El%20Golf%2C%20Las%20Condes&search_mode=regular_search&room_types%5B%5D=Entire%20home%2Fapt&selected_filter_order%5B%5D=room_types%3AEntire%20home%2Fapt&selected_filter_order%5B%5D=min_bedrooms%3A3&selected_filter_order%5B%5D=min_bathrooms%3A3&min_bedrooms=3&min_bathrooms=3
