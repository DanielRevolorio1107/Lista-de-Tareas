from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tareas(Base):
    __tablename__ = "tareas" #tabla en postgresql

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)
