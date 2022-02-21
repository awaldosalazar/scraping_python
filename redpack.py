from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


with sync_playwright() as p:
    cpDestination='45430'
    browser = p.chromium.launch(headless=True, slow_mo=100)
    
    # is open navigator and page
    page = browser.new_page()
    page.goto("https://www.redpack.com.mx/es/cobertura/")
    
    # write postal codes in origin and destination
    page.type("#cobertura_origen_cp","44330", delay=10)
    page.type("#cobertura_destino_cp",f"{cpDestination}", delay=10)
    
    page.click("button#cobertura_enviar")
    
    page.wait_for_timeout(5000)
    
    
    verifyCp = '[id="cobertura_error"]'
    coverage = '[id="cobertura_respuesta_servicios"]'
    delivery = '[id="cobertura_respuesta_entrega"]'
    typedelivery = '[id="cobertura_respuesta_cobertura"]'
    
    # Si la busqueda tiene error o no tiene cobertura no se muestra el componente
    error = page.is_visible(verifyCp)
    
    if error:
        print([{'Errror':True, 'Description':'NO SE TIENE COBERTURA PARA ESTE ENVÍO'}])
        page.screenshot(path=f"screenshots/error - {cpDestination}.png", full_page=True)
        page.close()
        browser.close()
        exit()
    
    # Seleccionamos los apartados de la tabla
    coverage = page.query_selector(coverage)
    delivery = page.query_selector(delivery)
    typedelivery = page.query_selector(typedelivery)
    html_covergae = coverage.inner_html()
    html_delivery = delivery.inner_html()
    html__type_delivery = typedelivery.inner_html()
    
    # Subs-traemos los parrafos por tabla
    soup_coverage = BeautifulSoup(html_covergae, 'html.parser')
    soup_delivery = BeautifulSoup(html_delivery, 'html.parser')
    soup_type_delivery = BeautifulSoup(html__type_delivery, 'html.parser')
    
    # Buscamos todos los parrafos
    total_coverage = soup_coverage.find_all('p') 
    total_delivery = soup_delivery.find_all('p') 
    total_type_delivery = soup_type_delivery.find_all('p') 
    
    coverages = []
    deliverys = []
    types_deliverys = []
    for c in total_coverage:
        detail = str(c)
        coverages.append(detail[3:len(detail)-4])
    
    for d in total_delivery:
        detail = str(d)
        deliverys.append(detail[3:len(detail)-4])
    
    for t in total_type_delivery:
        detail = str(t)
        types_deliverys.append(detail[3:len(detail)-4])
    
    schema = ({
        'coverage':coverages,
        'deliverys':deliverys,
        'types_deliverys':types_deliverys,
        'Error':False
    })
    
    
    print(schema)
    page.screenshot(path=f"screenshots/{cpDestination}.png", full_page=True)
    page.close()
    browser.close()