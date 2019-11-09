# IMPORTS
from Seazone.spiders.airbnb import AirbnbCrawl
from Seazone.spiders.vivareal import VivaRealCrawler
# URL's NECESSÁRIAS (INCLUINDO FILTROS)
AIR_URL_JURERE = 'Jurerê--Florianópolis-~-SC/homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&screen_size=large&search_type=filter_change&place_id=ChIJAwAnTFxEJ5UR-7iZMcQJ8I0&hide_dates_and_guests_filters=true&map_toggle=false&source=structured_search_input_header&adults=4&min_bedrooms=2'
AIR_URL_JURERE_INTERNACIONAL = 'Jurerê-Internacional--Florianópolis-~-SC/homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&screen_size=medium&search_type=pagination&map_toggle=false&source=structured_search_input_header&place_id=ChIJEdpFl_lEJ5URh3hkEEmIlVc&hide_dates_and_guests_filters=true&s_tag=V5gl7d_Q&adults=4&min_bedrooms=2&last_search_session_id=fced69c5-c226-4e10-81f4-e66f10e5311c'
VIVA_URL_JURERE = 'jurere/?pagina=1#onde=BR-Santa_Catarina-NULL-Florianopolis-Barrios-Jurere&quartos=2'
VIVA_URL_JURERE_INTERNACIONAL = 'jurere-internacional/?pagina=1#onde=BR-Santa_Catarina-NULL-Florianopolis-Barrios-Jurere_Internacional&quartos=2'

# INICIAR CAPTURA DOS DADOS
print("[INIT] Iniciando captura de dados Airbnb...")
air_crawler = AirbnbCrawl()
air_crawler.crawl_list_and_save([AIR_URL_JURERE, AIR_URL_JURERE_INTERNACIONAL])

# print("\n\n[INIT] Iniciando captura de dados Viva Real...")
# viva_crawler = VivaRealCrawler()
# viva_crawler.crawl_list_and_save([VIVA_URL_JURERE, VIVA_URL_JURERE_INTERNACIONAL])