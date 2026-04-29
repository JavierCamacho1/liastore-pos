import flet as ft
import sqlite3

def vista_login(on_login_success):
    txt_usuario = ft.TextField(label="Usuario", width=300)
    txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    lbl_error = ft.Text("", color=ft.Colors.RED)

    def intentar_login(e):
        usuario = txt_usuario.value
        password = txt_password.value

        try:
            conexion = sqlite3.connect("liastore_local.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT rol FROM usuarios WHERE username = ? AND password = ?", (usuario, password))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                rol = resultado[0]
                on_login_success(rol) # Enviamos el rol ('admin' o 'cajero') a main.py
            else:
                lbl_error.value = "Usuario o contraseña incorrectos."
                lbl_error.update()
        except Exception as ex:
            lbl_error.value = f"Error de BD: {ex}"
            lbl_error.update()

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0), 
        bgcolor=ft.Colors.GREY_50,
        content=ft.Card(
            elevation=5,
            content=ft.Container(
                padding=40,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.LOCK_PERSON, size=60, color=ft.Colors.BLUE_GREY_900),
                        ft.Text("LIASTORE POS", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Inicia sesión para continuar", color=ft.Colors.GREY_600),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        txt_usuario,
                        txt_password,
                        lbl_error,
                        ft.ElevatedButton(
                            content=ft.Text("Entrar", color=ft.Colors.WHITE), 
                            on_click=intentar_login, 
                            width=300, 
                            bgcolor=ft.Colors.BLUE_GREY_900
                        )
                    ]
                )
            )
        )
    )