import flet as ft

class Sidebar(ft.Container):
    # Ahora recibimos el 'rol' desde el Login
    def __init__(self, on_cambiar_vista, rol):
        super().__init__()
        self.on_cambiar_vista = on_cambiar_vista
        self.rol = rol 
        
        self.width = 250
        self.bgcolor = ft.Colors.BLUE_GREY_900
        self.padding = 20
        
        # 1. Botones base (Todos los ven)
        controles_menu = [
            ft.Text("LIASTORE", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(f"Rol: {self.rol.upper()}", size=12, color=ft.Colors.GREEN_400),
            ft.Divider(color=ft.Colors.WHITE24),
        ]
        
        # 2. Permisos de Administrador (Solo el dueño)
        if self.rol == 'admin':
            controles_menu.append(self._crear_boton("Dashboard", ft.Icons.DASHBOARD, "dashboard"))
            
        # 3. Permisos Generales (Todos pueden vender)
        controles_menu.append(self._crear_boton("Punto De Venta", ft.Icons.POINT_OF_SALE, "pos"))
        
        # 4. Más permisos de Administrador
        if self.rol == 'admin':
            controles_menu.append(self._crear_boton("Inventario", ft.Icons.INVENTORY_2, "inventario"))

        # NUEVO: Botón de Logout al fondo
        controles_menu.append(ft.Divider(color=ft.Colors.WHITE24))
        controles_menu.append(self._crear_boton("Cerrar Sesión", ft.Icons.LOGOUT, "logout"))
            
        self.content = ft.Column(
            controls=controles_menu,
            spacing=15
        )

    def _crear_boton(self, texto, icono, nombre_vista):
        return ft.TextButton(
            # Adaptado a Flet 0.84+: content debe ser un ft.Text, no un string
            content=ft.Text(texto, color=ft.Colors.WHITE), 
            icon=icono,
            icon_color=ft.Colors.WHITE,
            width=200,
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
            on_click=lambda e: self.on_cambiar_vista(nombre_vista)
        )