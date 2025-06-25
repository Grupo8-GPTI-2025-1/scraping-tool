from pi_scraper import PortalInmobiliarioScraper
from airbnb_scraper import AirbnbScraper

if __name__ == '__main__':
    print('Iniciando scrap...')
    portal_scraper = PortalInmobiliarioScraper()
    try:
        portal_scraper.post_portals()
    except Exception as e:
        print(f"Error en PortalInmobiliarioScraper: {e}\nEn caso de que se hayan cargado muy pocas propiedades, correr nuevamente el script.")
    portal_scraper.close()
    airbnb_scraper = AirbnbScraper()
    try:
        airbnb_scraper.post_airbnbs()
    except Exception as e:
        print(f"Error en AirbnbScraper: {e}\nEn caso de que se hayan cargado muy pocas propiedades, correr nuevamente el script.")
    airbnb_scraper.close()
    print('Scraping finalizado.')