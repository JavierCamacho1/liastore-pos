import flet as ft

from components.sidebar import Sidebar
from views.dashboard import vista_dashboard
from views.login import vista_login
from views.inventario import vista_inventario

def main(page: ft.Page):
    page.title = "LIASTORE - Punto de Venta"
    page.window_width = 1024
    page.window_height = 768
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    contenedor_raiz = ft.Container(expand=True)
    contenedor_vistas = ft.Container(expand=True)

    def cambiar_vista(nombre_vista):
        contenedor_vistas.content = None 
        if nombre_vista == "dashboard":
            contenedor_vistas.content = vista_dashboard()
        elif nombre_vista == "pos":
            contenedor_vistas.content = ft.Text("Aquí irá el Punto de Venta", size=30)
        elif nombre_vista == "inventario":
            contenedor_vistas.content = vista_inventario()
        elif nombre_vista == "logout":
            # Si dan clic en logout, volvemos a poner la vista de login en la raíz
            contenedor_raiz.content = vista_login(on_login_success=al_hacer_login)
        page.update()

    def al_hacer_login(rol):
        # 1. Le pasamos el rol al Menú Lateral
        menu_lateral = Sidebar(on_cambiar_vista=cambiar_vista, rol=rol)

        # 2. Ensamblamos la pantalla de trabajo
        layout = ft.Row(
            expand=True,
            spacing=0,
            controls=[menu_lateral, contenedor_vistas]
        )
        
        contenedor_raiz.content = layout
        
        # 3. Lógica de redirección por rol
        if rol == 'admin':
            cambiar_vista("dashboard") # El dueño quiere ver sus ganancias al entrar
        else:
            cambiar_vista("pos")       # El trabajador va directo a la caja registradora
            
        page.update()

    # Arrancamos mostrando solo el login
    contenedor_raiz.content = vista_login(on_login_success=al_hacer_login)
    page.add(contenedor_raiz)

if __name__ == "__main__":
    ft.run(main)