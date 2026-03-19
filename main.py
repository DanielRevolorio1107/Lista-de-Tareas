from http.client import responses
from fastapi import FastAPI, Depends
from pyexpat.errors import messages
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware #Intercambio de recursos de origen cruzado CORS
from database import engine, SessionLocal
import models, schemas
from fastapi import FastAPI , Depends, HTTPException #manejo de errore

# Crea las tablas si no existen
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Configuramos CORS para permitir que Angular se conecte
origenes_permitidos =[
"http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos los encabezados

)
# Esta función es nuestra "puerta de enlace" a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Siempre cerramos la conexión por seguridad

# Nuestra primera ruta CRUD: CREAR (Usamos @app.post)
@app.post("/tareas/")
def crear_tarea(tarea: schemas.TareaCrear, db: Session = Depends(get_db)):
    # 1. Convertimos el esquema (datos del usuario) al modelo (formato de BD)
    nueva_tarea = models.Tareas(titulo = tarea.titulo, descripcion=tarea.descripcion)
#agregamos y guardamos en la bd
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea) #para obtener el ID que le asigno postgresql

    return nueva_tarea

# Nuestra segunda ruta CRUD: LEER (Usamos @app.get)
@app.get("/tareas/", response_model=list[schemas.TareaRespuesta])
def leer_tareas(db: Session = Depends(get_db)):
#Le decimos a la base de datos: "Busca en el modelo Tarea y tráeme TODOS los registros"
    tareas = db.query(models.Tareas).all()
    return tareas

#Nuestra tercera ruta CRUD: ACTUALIZAR
@app.put("/tareas/{id}",response_model=schemas.TareaRespuesta)
def actualizar_tares(id: int, tarea_actualizada: schemas.TareaActualizar, db: Session = Depends(get_db)):
#1. Buscamos la tarea por su ID en la base de datos
    tarea_db = db.query(models.Tareas).filter(models.Tareas.id == id).first()

#2.Verificar si existe
    if tarea_db is None:
        raise HTTPException(status_code=404, detail="No se encuentra la tarea")
# 3. Actualizamos solo los datos que el usuario nos envió
    if tarea_actualizada.titulo is not None:
        tarea_db.titulo = tarea_actualizada.titulo
    if tarea_db.descripcion is not None:
        tarea_db.descripcion = tarea_actualizada.descripcion
    if tarea_db.completada is not None:
        tarea_db.completada = tarea_actualizada.completada
# 4. Guardamos los cambios en PostgreSQL
    db.commit()
    db.refresh(tarea_db)
    return tarea_db

# Nuestra cuarta y última ruta CRUD: ELIMINAR
@app.delete("/tareas/{id}")
def elimitar_tareas(id: int, db: Session = Depends(get_db)):
    #1.Buscar la tarea
    tarea_db = db.query(models.Tareas).filter(models.Tareas.id == id).first()

    #2.Verificar que exista
    if tarea_db is None:
        raise HTTPException(status_code=404, detail="No se encuentra la tarea")

    #3.le decimos a PostgreSQL que la borre y guardamos cambios
    db.delete(tarea_db)
    db.commit()

    return {"Tarea eliminada"}
