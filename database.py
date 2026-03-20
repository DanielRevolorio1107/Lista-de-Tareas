from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# El formato es: postgresql://usuario:contraseña@servidor:puerto/nombre_de_la_base_de_datos
# Buscamos la URL en la nube bajo el nombre "DATABASE_URL".
# Si no la encuentra (porque estás en tu compu), usa tu ruta local.
URL_BASE_DATOS = os.getenv(
"postgresql://postgres:daniuwu11@localhost:5432/gestor_tareas"
)

if URL_BASE_DATOS.startswith("postgres://"):
    URL_BASE_DATOS = URL_BASE_DATOS.replace("postgres://", "postgresql://", 1)

# El 'engine' es el motor que realmente maneja la comunicación con PostgreSQL
engine = create_engine(URL_BASE_DATOS)

# SessionLocal es como una "caseta de peaje": cada vez que queramos guardar o leer
# algo de la base de datos, abriremos una de estas sesiones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase principal de la que heredarán nuestros modelos (nuestras tablas)
Base = declarative_base()
