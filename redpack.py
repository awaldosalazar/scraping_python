from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

SCHEMA_MICRO = {
    "postal_code":"44330",
    "service":"REDPACK ECOEXPRESS",
    "delivery_type":"DOMICILIO",
    "extended_area":"False",
    "coverage":"True"
}

REDPACKECONOMICO = 'REDPACK ECOEXPRESS'
REDPACKEXPRESS = 'REDPACK EXPRESS'
OCURRE = 'SUCURSAL'
DOMICILIO = 'DOMICILIO'
NORMAL = 'NORMAL'

with sync_playwright() as p:
    cpDestination='44330'
    browser = p.chromium.launch(headless=True, slow_mo=100)
    
    # is open navigator and page
    page = browser.new_page()
    page.goto("https://www.redpack.com.mx/es/cobertura/")
    
    # write postal codes in origin and destination
    page.type("#cobertura_origen_cp","44330", delay=10)
    page.type("#cobertura_destino_cp",f"{cpDestination}", delay=10)
    
    page.click("button#cobertura_enviar")
    
    page.wait_for_timeout(10000)
    
    
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
    
    schema = {
        'coverage':coverages,
        'deliverys':deliverys,
        'types_deliverys':types_deliverys,
        'Error':False
    }
    
    arrayschema = []
    
    if not coverages:
        print('No tuvimos resultados')
    
    for type_coverage in coverages:
        if type_coverage == 'ECOEXPRESS':
            over_write_data = {
                **SCHEMA_MICRO.copy(),
                "postal_code": cpDestination,
                "service":  REDPACKECONOMICO,
                "delivery_type": DOMICILIO if DOMICILIO in deliverys else OCURRE,
                "extended_area":False if NORMAL in types_deliverys else True,
                "coverage":True
            }
            arrayschema.append(over_write_data)
        elif type_coverage == 'EXPRESS':
            over_write_data = {
                **SCHEMA_MICRO.copy(),
                "postal_code": cpDestination,
                "service":  REDPACKEXPRESS,
                "delivery_type": DOMICILIO if DOMICILIO in deliverys else OCURRE,
                "extended_area":False if NORMAL in types_deliverys else True,
                "coverage":True
            }
            arrayschema.append(over_write_data)
        # print(over_write_data)    
    print(arrayschema)
    # print(schema)
    # page.screenshot(path=f"screenshots/{cpDestination}.png", full_page=True)
    page.close()
    browser.close()