from fastapi import FastAPI, HTTPException
from backend.database import create_tables
from pydantic import BaseModel
import sqlite3

app = FastAPI()

create_tables()

class Socio(BaseModel):
    nombre: str
    apellido: str
    edad: int
    telefono: str | None = None
    mail: str | None = None
    fecha_registro: str

@app.get("/")
def inicio():
    return {"mensaje": "Sistema de gimnasio funcionando correctamente."}

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
    
@app.get("/Socios/{socio_id}")
def obtener_socios(socio_id: int):
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

@app.get("/socios")
def consultar_datos():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM socios")
    socios = cursor.fetchall()
    conn.close()
    return [dict(socio) for socio in socios]
    