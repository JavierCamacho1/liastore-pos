import flet as ft

import flet as ft

# Esta función simplemente dibuja y devuelve la pantalla del Dashboard.
def vista_dashboard():
    return ft.Container(
        expand=True, # Para que llene todo el espacio disponible a la derecha
        padding=30,
        content=ft.Column(
            controls=[
                ft.Text("Resumen del Día", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Métricas actualizadas desde SQLite.", size=16, color=ft.Colors.GREY_700),
                
                ft.Row(
                    controls=[
                        _crear_tarjeta_metrica("Ventas de Hoy", "$0.00", ft.Colors.GREEN_700),
                        _crear_tarjeta_metrica("Artículos", "0", ft.Colors.BLUE_700)
                    ],
                    spacing=20
                )
            ]
        )
    )

# función  para no repetir código visual.
def _crear_tarjeta_metrica(titulo, valor, color_valor):
    return ft.Card(
        content=ft.Container(
            padding=20,
            width=250,
            content=ft.Column([
                ft.Text(titulo, size=16, color=ft.Colors.GREY_600),
                ft.Text(valor, size=30, weight=ft.FontWeight.BOLD, color=color_valor)
            ])
        )
    )
            