import flet as ft
import sqlite3
import uuid

def vista_inventario():
    # CONTROLES
    txt_nombre = ft.TextField(label="Nombre del Producto", width=250)
    txt_precio = ft.TextField(label="Precio ($)", width=120)
    txt_stock = ft.TextField(label="Stock", width=100)
    
    drop_talla = ft.Dropdown(
        label="Talla", width=120, 
        options=[ft.dropdown.Option(t) for t in ["XS", "S", "M", "L", "XL", "Unitalla"]]
    )

    #  SECCIÓN DE COLOR
    drop_color = ft.Dropdown(
        label="Color", width=150, 
        options=[ft.dropdown.Option(c) for c in ["Blanco", "Negro", "Rojo", "Azul", "Beige", "Gris", "Otro..."]]
    )
    
    txt_color_custom = ft.TextField(label="Escribir color", width=150)
    btn_cancelar = ft.IconButton(icon=ft.Icons.CANCEL, icon_color=ft.Colors.RED_700, tooltip="Volver a la lista")
    row_custom = ft.Row(controls=[txt_color_custom, btn_cancelar], visible=False, spacing=0)
    seccion_color = ft.Row(controls=[drop_color, row_custom], spacing=0)

    #  FUNCIONES DENTRO de vista_inventario 
    def mostrar_custom(e):
        if drop_color.value == "Otro...":
            drop_color.visible = False
            row_custom.visible = True
            e.page.update()  

    def ocultar_custom(e=None):
        drop_color.value = None
        drop_color.visible = True
        row_custom.visible = False
        txt_color_custom.value = ""
        drop_color.update()
        row_custom.update()
        txt_color_custom.update()

    drop_color.on_change = mostrar_custom
    btn_cancelar.on_click = ocultar_custom

    lbl_mensaje = ft.Text("", color=ft.Colors.GREEN_600, weight=ft.FontWeight.BOLD)

    # TABLA 
    tabla_datos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Talla")),
            ft.DataColumn(ft.Text("Color")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
        ],
        rows=[]
    )

    # LÓGICA
    def cargar_inventario():
        tabla_datos.rows.clear()
        try:
            conexion = sqlite3.connect("liastore_local.db")
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT p.nombre, v.talla, v.color, p.precio_base, v.stock_actual
                FROM productos p
                JOIN variantes v ON p.id = v.producto_id
                ORDER BY p.nombre, v.talla
            ''')
            filas = cursor.fetchall()
            conexion.close()

            for fila in filas:
                tabla_datos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(fila[0])),
                            ft.DataCell(ft.Text(fila[1])),
                            ft.DataCell(ft.Text(fila[2])),
                            ft.DataCell(ft.Text(f"${fila[3]:.2f}")),
                            ft.DataCell(ft.Text(str(fila[4]))),
                        ]
                    )
                )
        except Exception as e:
            print(f"Error al cargar: {e}")

    def guardar_producto(e):
        if row_custom.visible:
            color_final = txt_color_custom.value.strip().capitalize()
        else:
            color_final = drop_color.value

        if not all([txt_nombre.value, txt_precio.value, txt_stock.value, drop_talla.value, color_final]) or color_final == "Otro...":
            lbl_mensaje.value = " Completa todos los campos con un color válido."
            lbl_mensaje.color = ft.Colors.RED
            lbl_mensaje.update()
            return

        try:
            conexion = sqlite3.connect("liastore_local.db")
            cursor = conexion.cursor()
            
            nombre_prod = txt_nombre.value.strip().upper()
            precio = float(txt_precio.value)
            stock = int(txt_stock.value)

            cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre_prod,))
            resultado = cursor.fetchone()

            if resultado:
                producto_id = resultado[0]
            else:
                producto_id = str(uuid.uuid4())
                cursor.execute('''
                    INSERT INTO productos (id, nombre, categoria, precio_base) 
                    VALUES (?, ?, 'Ropa', ?)
                ''', (producto_id, nombre_prod, precio))

            variante_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO variantes (id, producto_id, talla, color, stock_actual) 
                VALUES (?, ?, ?, ?, ?)
            ''', (variante_id, producto_id, drop_talla.value, color_final, stock))

            conexion.commit()
            conexion.close()

            txt_stock.value = ""
            drop_talla.value = None
            ocultar_custom()
            
            txt_stock.update()
            drop_talla.update()
            
            lbl_mensaje.value = "Variante agregada con éxito."
            lbl_mensaje.color = ft.Colors.GREEN
            lbl_mensaje.update()
            
            cargar_inventario()
            tabla_datos.update()

        except ValueError:
            lbl_mensaje.value = "⚠️ Precio y Stock deben ser números."
            lbl_mensaje.color = ft.Colors.RED
            lbl_mensaje.update()
        except Exception as ex:
            lbl_mensaje.value = f"Error de BD: {ex}"
            lbl_mensaje.color = ft.Colors.RED
            lbl_mensaje.update()

    cargar_inventario()

    return ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text("Gestión de Inventario", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Registra nuevos productos y sus variantes (Talla/Color).", color=ft.Colors.GREY_700),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    wrap=True,
                    controls=[
                        txt_nombre, 
                        txt_precio, 
                        drop_talla, 
                        seccion_color,
                        txt_stock,
                        ft.ElevatedButton(
                            content=ft.Text("Guardar", color=ft.Colors.WHITE), 
                            icon=ft.Icons.SAVE, 
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                            on_click=guardar_producto
                        )
                    ]
                ),
                lbl_mensaje,
                ft.Divider(color=ft.Colors.BLACK12),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[tabla_datos]
                    )
                )
            ]
        )
    )