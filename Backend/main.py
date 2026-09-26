#LENGUAJES Y BASES DE DATOS
from fastapi import FastAPI, HTTPException
from backend.database import create_tables
from pydantic import BaseModel
import sqlite3

#DAR ACCESO A FASTAPI CON ".APP"
app = FastAPI()

#IMPORTAR MODELO DE DATOS "DATABASE.PY"
create_tables()

#TESTEO 
@app.get("/")
def inicio():
    return {"mensaje": "Sistema de gimnasio funcionando correctamente."}


###PARTE QUE MANEJA LOS DATOS DE SOCIOS-----------------------

#AGREGAR SOCIO
class Socio(BaseModel):
    nombre: str
    apellido: str
    edad: int
    telefono: str | None = None
    mail: str | None = None
    fecha_registro: str
    
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

#CONSULTAR SOCIO PUNTUAL
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

#CONSULTAR SOCIOS
@app.get("/socios")
def consultar_datos():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM socios")
    socios = cursor.fetchall()
    conn.close()
    return [dict(socio) for socio in socios]

#ACTUALIZAR SOCIO
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

#ELIMINAR SOCIO
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
    
    
###PARTE QUE MANEJA LA PARTE DE MEMBRESIAS-------------------

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
    
    conn.close()
    

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
        (
        membresia.socio_id,
        membresia.tipo,
        membresia.fecha_inicio,
        membresia.fecha_vencimiento,
        membresia.precio,
        membresia.estado
        )
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
class ActualizarMembresia(BaseModel):
    tipo: str
    fecha_inicio: str
    fecha_vencimiento: str
    precio: float
    estado : str
    
@app.put("/membresias/{membresia_id}")
def actualizar_membresia(
    membresia_id: int,
    membresia: ActualizarMembresia
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
            membresia.estado,
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
@app.delete("/membresias/{membresia_id}")
def eliminar_membresia(membresia_id: int):
    conn = sqlite3.conect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM membresias WHERE id = ?",
        (membresia_id,)
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

#CRUD DE PAGOS-------------------------

#CREAR PAGOS
class Pago(BaseModel):
    socio_id: int
    membresia_id: int
    monto: float
    fecha_pago: str
    metodo_pago: str

@app.post("/pagos")
def crear_pagos(pago: Pago):
    conn = sqlite3.conect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO pagos(
            socio_id,
            membresia_id,
            monto,
            fecha_pago,
            metodo_pago
            )
            VALUES (?,?,?,?,?)
            """,
            (
                pago.socio_id,
                pago.membresia_id,
                pago.monto,
                pago.fecha_pago,
                pago.metodo_pago
            ))
    conn.commit()
    
    pago_id = cursor.lastrowid
    
    conn.close()
    
    return{
        "Mensaje": "Pago registrado correctamente",
        "id": pago_id
    }
    
#CONSULTAR PAGOS    
@app.get("/pagos")
def obtener_pagos():
        
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
        
    cursor.execute(" SELECT * FROM pagos")
        
    pagos= cursor.fetchall()
        
    conn.close()
    
    return [dict(pago) for pago in pagos]

@app.get("/pagos/{pago_id}")
def obtener_pago(pago_id: int):
    
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT FROM pagos WHERE id = ?",
        (pago_id,)
    )
    
    pago = cursor.fetchone()
    conn.close()
    
    if pago is None:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )
        
    return dict(pago)

#ACTUALIZAR PAGOS
class ActualizarPago(BaseModel):
    socio_id: int
    membresia_id: int
    monto: float
    fecha_pago: str
    metodo_pago: str
    
@app.put("/pagos/{pago_id}")
def actualizar_pago(
    pago_id: int,
    pago: ActualizarPago
):
    
    conn = sqlite3.conect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE pagos
        SET socio_id = ?,
        membresia_id = ?,
        monto = ?,
        fecha_pago = ?,
        metodo_pago = ?,
        WHERE id = ?
        """,
        (
        pago.socio_id,
        pago.membresia_id,
        pago.monto,
        pago.fecha_pago,
        pago.metodo_pago,
        pago_id
        ))
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )
        
    conn.close()
    
    return {
        "Mensaje": "Pago actualizado correctamente",
        "id": pago_id
    }
        
#ELIMINAR PAGOS        
@app.delete("/pagos/{pago_id}")
def eliminar_pago(pago_id : int):
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM pagos WHERE id = ?",
                   (pago_id)
    )
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )
        
    conn.close()
    
    return {
        "Mensaje": "Pago eliminado correctamente",
        "id": pago_id
    }
    
#CRUD ASISTENCIAS---------------------------------
    
#CREAR ASISTENCIA
class Asistencia(BaseModel):
    asistencia_id: int
    socio_id: int
    fecha: str
    hora: str
        
@app.post("/asistencias")
def crear_asistencia (asistencia: Asistencia):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO asistencias
                   socio_id,
                   fecha,
                   hora
                   )
                   VALUES (?,?,?)
                   """,
                   (
                    asistencia.socio_id,
                    asistencia.fecha,
                    asistencia.hora
                    )
    )
    conn.commit()
    
    asistencia_id = cursor.lastrowid()
    
    conn.close()
    
    return{
        "Mensaje": "Asistencia registrada exitosamente",
        "id": asistencia.asistencia_id
    }

#CONSULTAR ASISTENCIAS    
@app.get("/asistencias")
def consultar_asistencias():
    conn = sqlite3.connect*("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM asistencias")
    asistencias = cursor.fetchall()
    
    conn.close()
    
    return [dict(asistencia) for asistencia in asistencias ]


#CONSULTAR ASISTENCIA INDIVIDUAL  
@app.get("/asistencias/{asistencia_id}")
def consultar_asistencia (asistencia_id: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM asistencias WHERE id = ?",
                   (asistencia_id,)
                   )
    
    asistencia = cursor.fetchone()
    
    if asistencia is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Asistencia no encontrada"
        )
        
    conn.close()
    
    return dict(asistencia)


#ELIMINAR ASISTENCIA
@app.delete("/asistencias/{asistencia_id}")
def eliminar_asistencia(asistencia_id: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM asistencias WHERE id = ?",
                   (asistencia_id,)
    )
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Asistencia no encontrada"
        )
        
    conn.commit()
    conn.close()
    
    return{
        "Mensaje": "Asistencia eliminada correctamente",
        "id": asistencia_id
    }


    
    
      
    
    
    
    
    
    
    
    
        
    
    
    
