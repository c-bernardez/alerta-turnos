from getpass import getpass
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def main ():
    website = "https://www.hospitalitaliano.org.ar/#!/home/loginPortal"
    password = getpass("Contraseña: ") # evitamos guardarla en la historia del shell
    dni = os.getenv("DNI")
    apellido = os.getenv("LAST_NAME")
    centro = os.getenv("CENTER")

    with sync_playwright() as p:
        # iniciar navegador e ir al sitio web del Hospital Italiano
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(website)

        # iniciar sesión
        page.locator("#numeroDocumento").fill(dni)
        page.locator("#password").fill(password)
        page.get_by_role("button", name="Ingresar").click()

        # ir a la selección de turnos
        page.get_by_text("Turnos", exact=True).click()
        page.get_by_text("Reservar turnos", exact=True).click()
        page.get_by_role("link", name="CONTINUAR").click()

        # seleccionar tipo de consulta
        page.get_by_text("Consulta médica", exact=True).click()
        page.get_by_text("Profesional", exact=True).click()

        # seleccionar médico
        page.locator(".ui-select-match").click() 
        dr_search = page.locator(
            'input.ui-select-search[placeholder="Ingrese apellido"]'
        )
        dr_search.fill(apellido)

        doctor = page.locator(".ui-select-choices-row").filter(has_text="VICTORIO ROQUE") 
        doctor.wait_for(state="visible", timeout=10000) 
        doctor.click()      

        # seleccionar centro de atencion
        place_search = page.locator(
            '.ui-select-container[name="lugarDeAtencion"] input.ui-select-search'
        )
        place_search.fill(centro)

        place_option = page.locator(
            '.ui-select-container[name="lugarDeAtencion"] '
            '.ui-select-choices-row'
        ).filter(has_text=centro)
        place_option.wait_for(state="visible", timeout=10000)
        place_option.click()

        # buscar turnos
        page.get_by_role("button", name="Buscar turnos").click()

        # print info de proximos turnos
        page.locator(
            'input[name="turnoSeleccionado"]'
        ).first.wait_for(state="attached", timeout=15000)

        page.pause()

        browser.close()

if __name__ == "__main__":
    main( )

