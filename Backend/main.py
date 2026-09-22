#Lenguajes y base de datos
from fastapi import FastAPI, HTTPException
from backend.database import create_tables
from pydantic import BaseModel
import sqlite3

#Dar acceso a FastAPI con la palabra "app"
app = FastAPI()

#Importar modelos de tabla de database.py
create_tables()

#Estructura de la base de datos
class Socio(BaseModel):
    nombre: str
    apellido: str
    edad: int
    telefono: str | None = None
    mail: str | None = None
    fecha_registro: str

#Testeo de programa 
@app.get("/")
def inicio():
    return {"mensaje": "Sistema de gimnasio funcionando correctamente."}


###PARTE QUE MANEJA LOS DATOS DE SOCIOS-----------------------
#Agregar socio nuevo
@app.post("/socios")
def crear_socio(socio: Socio):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO socios(
            nombre,
            apellido,
            edad,
            telefono,
            mail,
            fecha_registro
            )
            VALUES(?,?,?,?,?,?)
            """,
            (socio.nombre,
             socio.apellido,
             socio.edad,
             socio.telefono,
             socio.mail,
             socio.fecha_registro
             )
         )
    
    
    conn.commit()

    socio_id = cursor.lastrowid

    conn.close()
    

    return {
    "mensaje":"Socio registrado correctamente",
    "id": socio_id
    }

#Consultar socio puntual
@app.get("/socios/{socio_id}")
def obtener_socio(socio_id: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM socios WHERE id = ?",
                   (socio_id, ) 
                   )
    
    socio = cursor.fetchone()
    conn.close()
    
    if socio is None:
        raise HTTPException(
            status_code=404,
            detail="Socio no encontrado"
        )
    
    return dict(socio) 

#Consultar base de datos
@app.get("/socios")
def consultar_datos():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM socios")
    socios = cursor.fetchall()
    conn.close()
    return [dict(socio) for socio in socios]

#Actualizar socio
class SocioActualizar(BaseModel):
    nombre : str
    apellido : str
    edad: int
    telefono : str | None = None
    mail : str | None = None
    
@app.put("/socios/{socio_id}")
def actualizar_socio(socio_id: int, socio: SocioActualizar):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE socios
        SET nombre = ?,
            apellido = ?,
            edad = ?,
            telefono = ?,
            mail = ?,
        WHERE id = ?
        """,
        (
            socio.nombre,
            socio.apellido,
            socio.edad,
            socio.telefono,
            socio.mail,
            socio_id
        )
    )
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        
        raise HTTPException(
            status_code=404,
            detail="Socio no encontrado"
        )
        
    return{
        "Mensaje": "Socio actualizado correctamente.",
        "id:": socio_id
    }

#Eliminar socio
@app.delete("/socio/{socio =_id}")
def eliminar_socio(socio_id: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM socios WHERE id = ?",
        (socio_id, )
        )
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        
        raise HTTPException(
            status_code=404,
            detail=" Socio no encontrado"
        )
    conn.close()
    
    return {
        "Mensaje": "Socio eliminado correctamente.",
        "id": socio_id
    }
    
    
###PARTE QUE MANEJA LA PARTE DE MEMBRESIAS

#CREAR MEMBRESIA
class Membresia(BaseModel):
    socio_id: int
    tipo : str
    fecha_inicio: str
    fecha_vencimiento: str 
    precio: float
    estado: str = "activa"
    
@app.post("/membresias")
def crear_membresia(membresia: Membresia):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT FROM socio WHERE id = ?",
        (membresia.socio_id,)
    )
    
    socio = cursor.fetchone()
        
    if socio is None:
        conn.close()
        
        raise HTTPException(
            status_code=404,
            detail= "El socio no existe"
        )
    
    #Registrar la membresia
    cursor.execute(
        """
        INSERT INTO membresias(
            socio_id,
            tipo,
            fecha_inicio,
            fecha_vencimiento,
            precio,
            estado
        )
        VALUES (?,?,?,?,?,?)
        """,
        (membresia.socio_id,
        membresia.tipo,
        membresia.fecha_inicio,
        membresia.fecha_vencimiento,
        membresia.precio,
        membresia.estado
        )
        
    conn.commit()
    
    membresia_id = cursor.lastrowid
    
    conn.close()
    
    return {
        "Mensaje": "Membresia registrada correctamente.",
        "id": membresia_id,
        "socio_id": membresia.socio_id
    }
    


#ACTUALIZAR MEMBRESIA
    
@app.put(/membresias,{membresia_id})
def actualizar_membresia(membresia_id: int,
                         mebresia: MembresiaActualizar)
):
    conn = sqlite3.conect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE membresias
        SET tipo = ?,
        fecha_inicio = ?,
        fecha_vencimineto = ?,
        precio = ?,
        estado = ?,
        WHERE id = ?
        """,
        (
            membresia.tipo,
            membresia.fecha_inicio,
            membresia.fecha_vencimiento,
            membresia.precio,
            membresia.estado
            membresia_id
        )
    )
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Membresia no encontrada"
        )
    
    conn.close()
    
    return{
        "Mensaje": "Membresia actualizada correctamente",
        "id": membresia_id
    }

#ELIMINAR MEMBRESIA 

@app.delete("/membresias,{membresia_id}")
def eliminar_membresia(membresia_id: int):
    conn = sqlite3.conect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM membresias WHERE id = ?",
        (membresia_id,)"
    )
    
    conn.commit()
    
    if cursor.rowcount == 0:
       conn.close()
    
       raise HTTPException(
                            status_code= 404,
                            detail= "Membresia no encontrada"
                         )
    
    conn.close()
    
    return{
        "Mensaje": "Membresia eliminada correctamente",
        "id": membresia_id
    }

