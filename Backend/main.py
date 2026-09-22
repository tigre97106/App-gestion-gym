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
