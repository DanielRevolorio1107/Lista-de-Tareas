from pydantic import BaseModel
from typing import Optional

# Este esquema define lo que le pedimos al usuario para CREAR una tarea
class TareaCrear(BaseModel):
    titulo: str
    descripcion: Optional[str] = None

class TareaRespuesta(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    completada : bool
    # Esta línea "mágica" le dice a Pydantic que lea los datos directamente
    # desde nuestro modelo de SQLAlchemy (la base de datos)
class Config:
    from_attributes = True

#esquema update
class TareaActualizar(BaseModel):
    titulo : Optional[str] = None
    descripcion: Optional[str] = None
    completada : bool

