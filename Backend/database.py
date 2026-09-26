import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    conn.execute('PRAGMA foreign_keys = ON;')  # Habilitar claves foráneas
    cursor = conn.cursor()

    #Crear tabla de socios
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            telefono TEXT,
            mail TEXT,
            fecha_registro TEXT NOT NULL    
        )
    ''')

    # Crear tabla de membresías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS membresias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            precio REAL NOT NULL,
            estado INTEGER
        )
    ''')

    # Crear tabla de pagos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER NOT NULL,
            membership_id INTEGER NOT NULL,
            fecha_pago TEXT NOT NULL,   
            fecha_vencimiento TEXT NOT NULL,
            FOREIGN KEY (socio_id) REFERENCES socios(id),
            FOREIGN KEY (membership_id) REFERENCES memberships(id)
        )
    ''')
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            FOREIGN KEY (socio_id) REFERENCES socios(id)
        )
    """)

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
        create_tables() 
        print("Tablas creadas correctamente en la base de datos.")


