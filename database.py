import sqlite3
import uuid

def inicializar_bd():
    conexion = sqlite3.connect("liastore_local.db")
    cursor = conexion.cursor()

    # 1. TABLA PRODUCTOS 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio_base REAL NOT NULL,
            imagen_url TEXT,
            activo BOOLEAN DEFAULT 1
        )
    ''')

    # 2. TABLA VARIANTES 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS variantes (
            id TEXT PRIMARY KEY,
            producto_id TEXT NOT NULL,
            talla TEXT NOT NULL,
            color TEXT NOT NULL,
            stock_actual INTEGER DEFAULT 0,
            sku_manual TEXT,
            sincronizado BOOLEAN DEFAULT 0,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    ''')

    # 3. TABLA USUARIOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, 
            rol TEXT NOT NULL,      
            activo BOOLEAN DEFAULT 1
        )
    ''')

    # 4. CREAR USUARIOS POR DEFECTO (Solo si la tabla está vacía)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        # Creamos un Admin (Dueño)
        cursor.execute('''
            INSERT INTO usuarios (id, username, password, rol)
            VALUES (?, 'admin', 'admin123', 'admin')
        ''', (str(uuid.uuid4()),))
        
        # Creamos un Cajero (Trabajador)
        cursor.execute('''
            INSERT INTO usuarios (id, username, password, rol)
            VALUES (?, 'cajero1', '1234', 'cajero')
        ''', (str(uuid.uuid4()),))
        print("✅ Usuarios por defecto creados (admin y cajero).")

    conexion.commit()
    conexion.close()
    print("✅ Base de datos 'liastore_local.db' inicializada y actualizada.")

if __name__ == "__main__":
    inicializar_bd()

#CREAS TU BD LOCAL CON ESTE ARCHIVO, LUEGO EJECUTAS main.py Y YA TE DEBERÍA FUNCIONAR EL LOGIN CON admin/admin123 O cajero1/1234. DESDE ALLÍ PUEDES PROBAR EL DASHBOARD Y EL INVENTARIO. SI QUIERES BORRAR LA BD Y EMPEZAR DE NUEVO, SOLO BORRA EL ARCHIVO liastore_local.db Y VUELVE A EJECUTAR ESTE database.py PARA RECREARLA CON LOS USUARIOS POR DEFECTO.
# python database.py